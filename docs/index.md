# 🫖 Teapot AI
### *Building AI-powered LLM agents, privately brewed in your browser.*

---

<!-- Announcement banner -->
<div style="
max-width: 980px;
margin: 10px auto 22px;
background: #ffffff;
border-radius: 999px;
padding: 12px 18px;
box-shadow: 0 10px 26px rgba(0,0,0,0.10);
font-size: 14px;
color: #111827;
">
🚀 <strong>Announcement:</strong> Our newest, tiniest model TinyTeapotLLM (77m params) Launched!
&nbsp; <a href="https://huggingface.co/teapotai/tinyteapot" style="font-weight:600;">Check out the Model →</a>
</div>

<!-- Hero -->
<div style="
max-width: 980px;
margin: 0 auto 34px;
background: #ffffff;
border-radius: 26px;
padding: 34px 32px;
box-shadow: 0 26px 70px rgba(0,0,0,0.14);
">

  <div style="
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 700;
  margin-bottom: 10px;
  ">
    Open Source Models · Enterprise Support
  </div>

  <h2 style="
  margin: 0 0 10px 0;
  font-size: 34px;
  line-height: 1.15;
  color: #111827;
  ">
    Lightweight models for fast, private AI.
  </h2>

  <p style="
  margin: 0 0 18px 0;
  font-size: 16px;
  line-height: 1.65;
  color: #374151;
  max-width: 760px;
  ">
    TeapotAI is an open-source ecosystem of ultra-efficient language models designed to run locally
    on CPUs, mobile devices, and in the browser — enabling low-latency, privacy-first AI without heavy GPU infrastructure.
  </p>

  <!-- CTA row -->
  <div style="display:flex; gap:14px; flex-wrap:wrap; margin-top: 18px;">
    <a href="/models" style="
      background:#111827;
      color:#ffffff;
      padding: 13px 22px;
      border-radius:999px;
      font-weight:700;
      text-decoration:none;
      box-shadow: 0 14px 34px rgba(0,0,0,0.18);
      ">
      🧠 Explore Models
    </a>

    <a href="/enterprise" style="
      background:#f3f4f6;
      color:#111827;
      padding: 13px 22px;
      border-radius:999px;
      font-weight:700;
      text-decoration:none;
      ">
      🏢 Enterprise & Deployment
    </a>
  </div>

  <!-- Proof bullets -->
  <div style="
  margin-top: 16px;
  font-size: 14px;
  color: #4b5563;
  ">
    ⚡ Ultra-low latency &nbsp;•&nbsp; 🔒 Privacy-first &nbsp;•&nbsp; 💸 Cost-efficient &nbsp;•&nbsp; 🫖 Open source
  </div>

</div>

<!-- What you can build -->
<div style="max-width:980px; margin: 0 auto 26px;">
  <h2 style="margin: 0 0 10px 0; color:#111827; font-size: 22px;">What you can build</h2>
  <p style="margin: 0 0 18px 0; color:#4b5563; font-size: 15px; max-width: 780px; line-height:1.6;">
    Teapot models are optimized for grounded reasoning and fast inference in real products.
  </p>

  <div style="display:grid; grid-template-columns: repeat(12, 1fr); gap: 16px;">
    <div style="grid-column: span 6; background:#ffffff; border-radius:20px; padding:18px 18px; box-shadow: 0 14px 36px rgba(0,0,0,0.10);">
      <div style="font-weight:800; color:#111827; margin-bottom:6px;">📚 In-context Q&A (RAG)</div>
      <div style="color:#4b5563; font-size:14px; line-height:1.6;">Grounded answers over your docs with low hallucination risk.</div>
    </div>

    <div style="grid-column: span 6; background:#ffffff; border-radius:20px; padding:18px 18px; box-shadow: 0 14px 36px rgba(0,0,0,0.10);">
      <div style="font-weight:800; color:#111827; margin-bottom:6px;">🧾 JSON extraction</div>
      <div style="color:#4b5563; font-size:14px; line-height:1.6;">Structured outputs from messy text: forms, logs, tickets, notes.</div>
    </div>

    <div style="grid-column: span 6; background:#ffffff; border-radius:20px; padding:18px 18px; box-shadow: 0 14px 36px rgba(0,0,0,0.10);">
      <div style="font-weight:800; color:#111827; margin-bottom:6px;">🏷️ Classification & routing</div>
      <div style="color:#4b5563; font-size:14px; line-height:1.6;">Intent detection, tagging, moderation, triage, and automation.</div>
    </div>

    <div style="grid-column: span 6; background:#ffffff; border-radius:20px; padding:18px 18px; box-shadow: 0 14px 36px rgba(0,0,0,0.10);">
      <div style="font-weight:800; color:#111827; margin-bottom:6px;">📊 Retrieval, ranking & search</div>
      <div style="color:#4b5563; font-size:14px; line-height:1.6;">Fast scoring/reranking where latency budgets are tight.</div>
    </div>
  </div>

  <div style="margin-top: 12px; color:#6b7280; font-size: 13px;">
    Want help deploying any of these? See <a href="/enterprise" style="font-weight:600;">Enterprise</a>.
  </div>
</div>

---

# Teapot LLM

Teapot is a small open-source language model (~800M parameters) fine-tuned on synthetic data and optimized to run locally on resource-constrained devices such as smartphones, browsers, and CPUs.

- 🔎 Grounded Q&A and Retrieval-Augmented Generation (RAG)
- 🧾 Structured extraction (JSON)
- ⚡ Efficient inference for production workloads

![./assets/teapot_diagram.png](./assets/teapot_diagram.png)

<div style="max-width: 980px; margin: 24px auto 0; display:flex; gap:12px; flex-wrap:wrap;">
  <a href="/models" style="
    background:#111827;
    color:#ffffff;
    padding: 13px 22px;
    border-radius:999px;
    font-weight:700;
    text-decoration:none;
    box-shadow: 0 14px 34px rgba(0,0,0,0.18);
    ">
    🧠 View all models
  </a>
  <a href="/enterprise" style="
    background:#f3f4f6;
    color:#111827;
    padding: 13px 22px;
    border-radius:999px;
    font-weight:700;
    text-decoration:none;
    ">
    🏢 Enterprise support
  </a>
</div>
