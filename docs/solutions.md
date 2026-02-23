---
title: Enterprise
---

<style>
  :root{
    --bg: #0b0f14;
    --panel: rgba(255,255,255,0.06);
    --panel2: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.10);
    --text: rgba(255,255,255,0.92);
    --muted: rgba(255,255,255,0.70);
    --muted2: rgba(255,255,255,0.58);
    --shadow: 0 10px 35px rgba(0,0,0,0.35);
    --radius: 18px;
  }

  /* Page wrapper */
  .tp-wrap{
    max-width: 1080px;
    margin: 0 auto;
    padding: 22px 16px 56px;
    color: var(--text);
  }

  /* Hero */
  .tp-hero{
    border: 1px solid var(--border);
    background: linear-gradient(180deg, var(--panel), var(--panel2));
    border-radius: calc(var(--radius) + 6px);
    box-shadow: var(--shadow);
    padding: 26px 22px;
  }
  .tp-kicker{
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted2);
    margin: 0 0 10px 0;
  }
  .tp-title{
    font-size: 34px;
    line-height: 1.15;
    margin: 0 0 10px 0;
  }
  .tp-subtitle{
    font-size: 16px;
    line-height: 1.55;
    color: var(--muted);
    margin: 0 0 18px 0;
    max-width: 78ch;
  }

  /* Buttons */
  .tp-actions{
    display:flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
  }
  .tp-btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap: 8px;
    padding: 10px 14px;
    border-radius: 999px;
    border: 1px solid var(--border);
    text-decoration:none;
    font-weight: 600;
    font-size: 14px;
    color: var(--text);
    background: rgba(255,255,255,0.06);
  }
  .tp-btn:hover{ transform: translateY(-1px); }
  .tp-btn-primary{
    background: rgba(255,255,255,0.92);
    color: #0b0f14 !important;
    border-color: rgba(255,255,255,0.0);
  }
  .tp-btn-primary:hover{ opacity: 0.95; }

  /* Section */
  .tp-section{
    margin-top: 18px;
  }
  .tp-h2{
    font-size: 18px;
    margin: 0 0 10px 0;
  }
  .tp-note{
    color: var(--muted2);
    font-size: 13px;
    line-height: 1.55;
    margin: 0 0 14px 0;
  }

  /* Grid / Cards */
  .tp-grid{
    display:grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 12px;
  }
  .tp-card{
    grid-column: span 6;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.05);
    border-radius: var(--radius);
    padding: 16px 16px 14px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
  }
  .tp-card h3{
    margin: 0 0 6px 0;
    font-size: 16px;
  }
  .tp-card p{
    margin: 0 0 10px 0;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.55;
  }
  .tp-bullets{
    margin: 0;
    padding-left: 18px;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.55;
  }
  .tp-bullets li{ margin: 6px 0; }

  /* Full width cards */
  .tp-card-wide{ grid-column: span 12; }

  /* CTA Footer */
  .tp-cta{
    margin-top: 18px;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
    border-radius: calc(var(--radius) + 6px);
    padding: 18px 16px;
    box-shadow: var(--shadow);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 14px;
    flex-wrap: wrap;
  }
  .tp-cta strong{ font-size: 16px; }
  .tp-cta span{
    display:block;
    margin-top: 4px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.5;
    max-width: 80ch;
  }

  @media (max-width: 860px){
    .tp-card{ grid-column: span 12; }
    .tp-title{ font-size: 28px; }
  }
</style>

<div class="tp-wrap">

  <div class="tp-hero">
    <p class="tp-kicker">Open source models • Paid enterprise support</p>
    <h1 class="tp-title">Enterprise TeapotAI</h1>
    <p class="tp-subtitle">
      TeapotAI helps teams deploy fast, private, and cost-efficient AI using the Teapot model family.
      Our models are optimized for <strong>ultra-low latency</strong> and can run on <strong>client devices</strong>
      (CPU, mobile, browser) — ideal when privacy, cost, and responsiveness matter.
    </p>

    <div class="tp-actions">
      <a class="tp-btn tp-btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI%20Enterprise%20Inquiry">Contact Sales</a>
      <a class="tp-btn" href="/models">Explore Models</a>
      <a class="tp-btn" href="/docs.html">Read Docs</a>
    </div>

    <p class="tp-note" style="margin-top:12px;">
      Teapot models are free to use. Organizations pay us when they want help with deployment, fine-tuning,
      hosting, evaluation, and long-term support.
    </p>
  </div>

  <div class="tp-section">
    <h2 class="tp-h2">What we do</h2>
    <p class="tp-note">
      We partner with product and ML teams end-to-end: architecture → model alignment → productionization → support.
      Typical timelines range from fast proof-of-concept to full production rollout.
    </p>

    <div class="tp-grid">
      <div class="tp-card">
        <h3>⚡ Deployment & Productionization</h3>
        <p>Get Teapot running in your stack with predictable latency and clean integration patterns.</p>
        <ul class="tp-bullets">
          <li>On-device inference (mobile / browser / edge)</li>
          <li>CPU-optimized hosting and batching</li>
          <li>RAG pipelines (retrieval, chunking, caching)</li>
          <li>Monitoring, evals, and regression testing</li>
        </ul>
      </div>

      <div class="tp-card">
        <h3>🧠 Custom Fine-Tuning & Alignment</h3>
        <p>Make the model behave the way your product needs: formatting, tone, refusals, and domain workflows.</p>
        <ul class="tp-bullets">
          <li>Instruction tuning & domain specialization</li>
          <li>Grounded QA / extraction tuning</li>
          <li>Dataset design (incl. synthetic augmentation)</li>
          <li>Benchmarking + acceptance criteria</li>
        </ul>
      </div>

      <div class="tp-card">
        <h3>🔒 Private AI & Compliance</h3>
        <p>Keep sensitive data local. Reduce exposure by avoiding third-party API calls.</p>
        <ul class="tp-bullets">
          <li>On-prem / air-gapped deployments</li>
          <li>Device-local inference and retrieval</li>
          <li>PII-aware pipelines and auditability</li>
          <li>Security review + threat modeling support</li>
        </ul>
      </div>

      <div class="tp-card">
        <h3>📚 Enterprise RAG & Knowledge Systems</h3>
        <p>Turn internal docs into trustworthy assistants with grounded answers and structured outputs.</p>
        <ul class="tp-bullets">
          <li>Knowledge-base Q&A assistants</li>
          <li>Document understanding + extraction (JSON)</li>
          <li>Hybrid retrieval strategies + reranking</li>
          <li>Latency/cost optimization at scale</li>
        </ul>
      </div>

      <div class="tp-card tp-card-wide">
        <h3>Why Teapot models</h3>
        <p>
          Teapot is built for real production constraints — not just cloud GPUs. It’s optimized for low-latency,
          grounded responses and can run in environments where large models are too slow, too expensive, or too risky.
        </p>
        <div class="tp-grid" style="margin-top:10px;">
          <div class="tp-card" style="grid-column: span 4;">
            <h3>🚀 Speed</h3>
            <p>Low-latency inference, including CPU + edge scenarios where response time matters.</p>
          </div>
          <div class="tp-card" style="grid-column: span 4;">
            <h3>🔐 Privacy</h3>
            <p>Run locally to keep user and company data on-device or inside your network boundary.</p>
          </div>
          <div class="tp-card" style="grid-column: span 4;">
            <h3>💸 Cost</h3>
            <p>Reduce or eliminate per-token API spend with efficient deployment and lightweight models.</p>
          </div>
        </div>
      </div>

    </div>
  </div>

  <div class="tp-section">
    <h2 class="tp-h2">Engagement models</h2>
    <p class="tp-note">Pick what fits your org. We can start small and expand once value is proven.</p>

    <div class="tp-grid">
      <div class="tp-card">
        <h3>Starter</h3>
        <p>Best for teams deploying Teapot for the first time.</p>
        <ul class="tp-bullets">
          <li>Architecture + integration plan</li>
          <li>Deployment support</li>
          <li>Baseline eval harness</li>
        </ul>
      </div>

      <div class="tp-card">
        <h3>Production</h3>
        <p>Best for live product workloads and performance targets.</p>
        <ul class="tp-bullets">
          <li>Latency/cost optimization</li>
          <li>RAG tuning + caching strategies</li>
          <li>Monitoring + regression evals</li>
        </ul>
      </div>

      <div class="tp-card tp-card-wide">
        <h3>Custom</h3>
        <p>For fine-tuning, proprietary workflows, or complex compliance requirements.</p>
        <ul class="tp-bullets">
          <li>Custom fine-tuning + alignment</li>
          <li>On-prem / air-gapped deployment</li>
          <li>Dedicated support and roadmap collaboration</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="tp-cta">
    <div>
      <strong>Ready to deploy TeapotAI in production?</strong>
      <span>
        Tell us your use case, latency target, and deployment environment (mobile, browser, CPU, on-prem, cloud).
        We’ll respond with a recommended plan and next steps.
      </span>
    </div>
    <div class="tp-actions" style="margin:0;">
      <a class="tp-btn tp-btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI%20Enterprise%20Inquiry">Contact Sales</a>
      <a class="tp-btn" href="mailto:hello@teapotai.com?subject=TeapotAI%20Enterprise%20-%20Request%20a%20demo">Request a Demo</a>
    </div>
  </div>

</div>
