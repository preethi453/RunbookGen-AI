def build_prompt(query, docs):
    context_blocks = []
    for i, doc in enumerate(docs, start=1):
        if isinstance(doc, dict):
            text = doc.get("text", "")
            source = doc.get("source", "Red Hat documentation")
            score = doc.get("score", "")
            context_blocks.append(f"[Doc {i} | Source: {source} | Score: {score}]\n{text}")
        else:
            context_blocks.append(f"[Doc {i}]\n{doc}")

    context = "\n\n".join(context_blocks) if context_blocks else "No matching documentation was retrieved. Use safe general Linux troubleshooting steps."

    return f"""
You are RunbookGen AI, a senior Linux and Red Hat support engineer.
Create a production-ready troubleshooting runbook for a junior engineer.

User issue:
{query}

Retrieved documentation context:
{context}

Strict rules:
- Use the retrieved documentation only when it is relevant to the issue.
- Do not copy long raw documentation text.
- Do not invent destructive commands.
- Prefer safe diagnostic commands before restart, deletion, permission, firewall, or SELinux changes.
- Mention impact before service restart, firewall change, SELinux change, or configuration change.
- Use simple professional language.
- Keep commands realistic for Linux/RHEL.
- If the exact service name is unknown, use placeholders like <service-name>.

Required output format exactly:

Issue Title:

Problem Summary:

Environment / Assumptions:

Possible Causes:

Step-by-Step Troubleshooting:
1.
2.
3.
4.
5.

Commands:

Risk Warnings:

Rollback Plan:

Validation Steps:

Escalation Notes:
"""
