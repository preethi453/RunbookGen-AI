import re
from typing import Dict, List, Tuple

from llm_client import LLMError, generate_with_ollama
from prompt_template import build_prompt


SERVICE_HINTS = {
    "apache": "httpd",
    "httpd": "httpd",
    "nginx": "nginx",
    "mysql": "mysqld",
    "mariadb": "mariadb",
    "docker": "docker",
    "podman": "podman",
    "ssh": "sshd",
    "firewall": "firewalld",
    "firewalld": "firewalld",
}


REQUIRED_SECTIONS = [
    "Issue Title:",
    "Problem Summary:",
    "Environment / Assumptions:",
    "Possible Causes:",
    "Step-by-Step Troubleshooting:",
    "Commands:",
    "Risk Warnings:",
    "Rollback Plan:",
    "Validation Steps:",
    "Escalation Notes:",
]


def detect_service(query: str) -> str:
    q = query.lower()
    for key, service in SERVICE_HINTS.items():
        if key in q:
            return service
    return "<service-name>"


def detect_issue_type(query: str) -> str:
    q = query.lower()

    if any(word in q for word in ["apache", "httpd", "nginx", "web server"]):
        return "web_service"
    if any(word in q for word in ["docker", "container", "podman"]):
        return "container"
    if any(word in q for word in ["selinux", "permission denied", "avc"]):
        return "selinux"
    if any(word in q for word in ["port", "firewall", "connection refused", "network"]):
        return "network"
    if any(word in q for word in ["disk", "space", "storage", "mount"]):
        return "storage"

    return "general"


def extract_doc_hints(docs: List[Dict[str, object]]) -> List[str]:
    hints = []

    keywords = [
        "systemctl",
        "journalctl",
        "firewall-cmd",
        "getenforce",
        "setsebool",
        "semanage",
        "restorecon",
        "ss -",
        "curl",
        "podman",
        "docker",
        "apachectl",
    ]

    for doc in docs:
        text = doc.get("text", "") if isinstance(doc, dict) else str(doc)
        sentences = re.split(r"(?<=[.!?])\s+", text)

        for sentence in sentences:
            lower = sentence.lower()

            if any(k in lower for k in keywords) and len(sentence) < 240:
                clean = sentence.strip(" -•\t")

                if clean and clean not in hints:
                    hints.append(clean)

            if len(hints) >= 4:
                return hints

    return hints


def build_commands(issue_type: str, service: str) -> List[str]:
    common = [
        f"systemctl status {service}",
        f"journalctl -u {service} -n 80 --no-pager",
    ]

    if issue_type == "web_service":
        return common + [
            "apachectl configtest  # Apache/httpd only",
            "ss -tulnp | grep -E ':80|:443'",
            "firewall-cmd --list-all",
            f"systemctl restart {service}",
        ]

    if issue_type == "container":
        return [
            "docker ps -a  # or: podman ps -a",
            "docker logs <container_id>",
            "docker inspect <container_id>",
            "ss -tulnp",
            "docker restart <container_id>",
        ]

    if issue_type == "selinux":
        return common + [
            "getenforce",
            "ausearch -m avc -ts recent",
            "restorecon -Rv <affected_path>",
            "semanage fcontext -l | grep <path_or_service>",
        ]

    if issue_type == "network":
        return common + [
            "ss -tulnp",
            "firewall-cmd --list-all",
            "curl -I http://localhost",
            "ping <server_ip>",
        ]

    if issue_type == "storage":
        return [
            "df -h",
            "du -sh <path>",
            "lsblk",
            "mount | column -t",
            "journalctl -xe --no-pager",
        ]

    return common + [
        "journalctl -xe --no-pager",
        "ss -tulnp",
        "df -h",
        f"systemctl restart {service}",
    ]


def validate_output(text: str) -> bool:
    lower = text.lower()
    return all(section.lower() in lower for section in REQUIRED_SECTIONS[:7])


def fallback_runbook(query: str, docs: List[Dict[str, object]], reason: str = "") -> str:
    issue_type = detect_issue_type(query)
    service = detect_service(query)
    commands = build_commands(issue_type, service)
    doc_hints = extract_doc_hints(docs)

    possible_causes = {
        "web_service": [
            "Service is stopped or failed",
            "Syntax error in web server configuration",
            "Port 80/443 conflict",
            "Firewall rule missing",
            "SELinux policy blocking access",
        ],
        "container": [
            "Container is stopped",
            "Application inside container crashed",
            "Wrong port mapping",
            "Image or volume issue",
            "Network bridge problem",
        ],
        "selinux": [
            "SELinux denial",
            "Wrong file context",
            "Boolean policy not enabled",
            "Service trying to access restricted path",
        ],
        "network": [
            "Service not listening",
            "Firewall blocking the port",
            "Wrong IP/port configuration",
            "DNS or routing issue",
        ],
        "storage": [
            "Disk full",
            "Mount point unavailable",
            "Permission issue",
            "Large logs or temporary files",
        ],
        "general": [
            "Service failure",
            "Configuration issue",
            "Permission issue",
            "Resource issue",
            "Recent system change",
        ],
    }[issue_type]

    lines = []

    lines.append("Issue Title:")
    lines.append(f"{query.strip().capitalize()} - Troubleshooting Runbook\n")

    lines.append("Problem Summary:")
    lines.append(
        f"The reported issue is: '{query}'. This runbook provides safe diagnosis and recovery steps."
    )
    lines.append("")

    lines.append("Environment / Assumptions:")
    lines.append("- Linux/RHEL-based server")
    lines.append(f"- Target service: {service}")
    lines.append("- Engineer has sudo/root access\n")

    lines.append("Possible Causes:")
    for cause in possible_causes:
        lines.append(f"- {cause}")

    if doc_hints:
        lines.append("\nDocumentation-Based Hints:")
        for hint in doc_hints:
            lines.append(f"- {hint}")

    lines.append("\nStep-by-Step Troubleshooting:")
    steps = [
        "Confirm exact error, host, service name, and recent changes.",
        "Check service status before changing anything.",
        "Review recent logs and identify the first useful error.",
        "Validate configuration files before restart.",
        "Check firewall, SELinux, ports, disk space, and permissions.",
        "Apply the smallest safe fix and record it.",
        "Restart only the affected service after impact check.",
        "Validate from local and client side.",
    ]

    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")

    lines.append("\nCommands:")
    for cmd in commands:
        lines.append(f"- {cmd}")

    lines.append("\nRisk Warnings:")
    lines.append("- Restarting services may interrupt users.")
    lines.append("- Firewall or SELinux changes can block or expose services.")
    lines.append("- Do not delete files or change permissions without backup/approval.\n")

    lines.append("Rollback Plan:")
    lines.append("- Backup config files before editing.")
    lines.append("- Revert changed files/settings if validation fails.")
    lines.append(f"- Restart {service} again only if configuration was changed.\n")

    lines.append("Validation Steps:")
    lines.append(f"- Confirm '{query}' is resolved.")
    lines.append(f"- Run systemctl status {service} if applicable.")
    lines.append("- Recheck logs for new critical errors.")
    lines.append("- Test from user/client side.\n")

    lines.append("Escalation Notes:")
    lines.append(
        "- Escalate if issue repeats, affects multiple servers, or shows kernel/storage/security errors."
    )
    lines.append(
        "- Attach logs, command outputs, recent changes, and documentation references."
    )

    return "\n".join(lines)


def generate_runbook(
    query: str,
    docs: List[Dict[str, object]],
    use_llm: bool = True
) -> Tuple[str, str]:
    """Return (runbook_text, generation_mode)."""

    prompt = build_prompt(query, docs)

    if use_llm:
        try:
            answer = generate_with_ollama(prompt)

            if validate_output(answer):
                return answer, "Ollama GenAI + RAG"

            return (
                fallback_runbook(query, docs),
                "Fallback after LLM validation",
            )

        except LLMError:
            return (
                fallback_runbook(query, docs),
                "Fallback; Ollama unavailable",
            )

    return fallback_runbook(query, docs), "Rule-based fallback"