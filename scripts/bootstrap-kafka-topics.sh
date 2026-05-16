#!/usr/bin/env bash
set -euo pipefail

# Create required Kafka topics via MSK bootstrap brokers.
# Topics are created here, NOT in Terraform.
# Usage: ./scripts/bootstrap-kafka-topics.sh <bootstrap-brokers-sasl-scram>
#
# REGULATORY: rwa.audit.events retention = 365 days — NEVER reduce.
# Requires: kafka-topics.sh on PATH, or docker run bitnami/kafka.

BOOTSTRAP_BROKERS="${1:-}"
if [[ -z "${BOOTSTRAP_BROKERS}" ]]; then
  echo "ERROR: Bootstrap brokers argument required." >&2
  echo "Usage: $0 <bootstrap-broker-string>" >&2
  echo "Get from: terraform output -raw bootstrap_brokers_sasl_scram" >&2
  exit 1
fi

if [[ -z "${MSK_USERNAME:-}" ]] || [[ -z "${MSK_PASSWORD:-}" ]]; then
  echo "ERROR: MSK_USERNAME and MSK_PASSWORD must be set." >&2
  exit 1
fi

# Write JAAS config to temp file (never printed to stdout)
JAAS_FILE="$(mktemp)"
trap 'rm -f "${JAAS_FILE}"' EXIT
cat > "${JAAS_FILE}" <<EOF
KafkaClient {
  org.apache.kafka.common.security.scram.ScramLoginModule required
  username="${MSK_USERNAME}"
  password="${MSK_PASSWORD}";
};
EOF

KAFKA_OPTS="-Djava.security.auth.login.config=${JAAS_FILE}"
COMMON_OPTS="--bootstrap-server ${BOOTSTRAP_BROKERS} --command-config /dev/stdin"

kafka_topic() {
  local topic="$1"
  local partitions="$2"
  local retention_ms="$3"

  echo "==> Topic: ${topic} (${partitions} partitions, retention ${retention_ms}ms)"

  if kafka-topics.sh --bootstrap-server "${BOOTSTRAP_BROKERS}" \
      --command-config <(echo "security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
${KAFKA_OPTS}") \
      --describe --topic "${topic}" 2>/dev/null | grep -q "${topic}"; then
    echo "    Already exists, updating retention only."
    kafka-configs.sh \
      --bootstrap-server "${BOOTSTRAP_BROKERS}" \
      --command-config <(echo "security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512") \
      --entity-type topics \
      --entity-name "${topic}" \
      --alter \
      --add-config "retention.ms=${retention_ms}" 2>/dev/null || true
  else
    KAFKA_OPTS="${KAFKA_OPTS}" kafka-topics.sh \
      --bootstrap-server "${BOOTSTRAP_BROKERS}" \
      --command-config <(echo "security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512") \
      --create \
      --topic "${topic}" \
      --partitions "${partitions}" \
      --replication-factor 1 \
      --config "retention.ms=${retention_ms}"
    echo "    Created."
  fi
}

DAYS_7=$((7 * 24 * 60 * 60 * 1000))
DAYS_30=$((30 * 24 * 60 * 60 * 1000))
DAYS_90=$((90 * 24 * 60 * 60 * 1000))
# REGULATORY: 365 days — NEVER reduce this value
DAYS_365=$((365 * 24 * 60 * 60 * 1000))

kafka_topic "rwa.calculations.requests"  12 "${DAYS_7}"
kafka_topic "rwa.calculations.results"   12 "${DAYS_30}"
kafka_topic "rwa.audit.events"            6 "${DAYS_365}"  # REGULATORY — BCBS239, EBA GL, DORA Art.6
kafka_topic "rwa.compliance.events"       3 "${DAYS_90}"
kafka_topic "rwa.data.lineage"            3 "${DAYS_7}"

echo ""
echo "==> Kafka topics bootstrap complete."
