## Looking for Enterprise support?

<style>
.enterprise-wrap{
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 64px;
  color: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Hero Container */
.enterprise-hero{
  background: #ffffff;
  border-radius: 28px;
  padding: 34px 30px;
  box-shadow: 0 25px 70px rgba(0,0,0,0.15);
}

/* Typography */
.kicker{
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 10px;
}

.hero-title{
  font-size: 40px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #111827;
}

.hero-subtitle{
  font-size: 17px;
  line-height: 1.6;
  color: #374151;
  max-width: 760px;
  margin-bottom: 20px;
}

.hero-note{
  font-size: 14px;
  color: #6b7280;
  margin-top: 14px;
}

/* Buttons */
.cta-row{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.btn-primary{
  background: #111827;
  color: #ffffff !important;
  padding: 12px 20px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s ease;
}

.btn-primary:hover{
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.btn-secondary{
  background: #f3f4f6;
  color: #111827;
  padding: 12px 20px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
}

/* Sections */
.section{
  margin-top: 46px;
}

.section h2{
  font-size: 26px;
  color: #111827;
  margin-bottom: 10px;
}

.section p{
  color: #4b5563;
  font-size: 15px;
  max-width: 820px;
  margin-bottom: 28px;
  line-height: 1.6;
}

/* Use Case Cards */
.usecase-grid{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
}

.usecase-card{
  grid-column: span 6;
  background: #ffffff;
  border-radius: 22px;
  padding: 22px 22px;
  box-shadow: 0 16px 40px rgba(0,0,0,0.12);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.usecase-card:hover{
  transform: translateY(-3px);
  box-shadow: 0 22px 50px rgba(0,0,0,0.18);
}

.usecase-title{
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.usecase-desc{
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
}

/* CTA Banner */
.enterprise-cta{
  margin-top: 60px;
  background: #ffffff;
  border-radius: 28px;
  padding: 36px 30px;
  text-align: center;
  box-shadow: 0 25px 70px rgba(0,0,0,0.15);
}

.enterprise-cta h3{
  font-size: 30px;
  color: #111827;
  margin-bottom: 12px;
}

.enterprise-cta p{
  font-size: 16px;
  color: #4b5563;
  margin-bottom: 24px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

/* Mobile */
@media (max-width: 900px){
  .usecase-card{
    grid-column: span 12;
  }
  .hero-title{
    font-size: 32px;
  }
}
</style>

<div class="enterprise-wrap">

<!-- HERO -->
<div class="enterprise-hero">
  <div class="kicker">Open Source Models · Enterprise Support</div>
  <div class="hero-title">Enterprise TeapotAI</div>
  <div class="hero-subtitle">
    TeapotAI helps organizations deploy ultra-low latency AI that runs locally on CPUs, mobile devices,
    and browsers. Our Teapot model family is optimized for private, cost-efficient, and production-grade
    inference — without relying on expensive cloud APIs or large GPU infrastructure.
  </div>

  <div class="cta-row">
    <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
      Contact Sales
    </a>
    <a class="btn-secondary" href="/models">
      View Models
    </a>
  </div>

  <div class="hero-note">
    Teapot models are open source. Organizations reach out when they need deployment, fine-tuning,
    hosting, evaluation, or enterprise support.
  </div>
</div>

<!-- USE CASES -->
<div class="section">
  <h2>Enterprise Use Cases</h2>
  <p>
    Teapot models are designed for real-world production systems where latency, privacy, and cost constraints matter.
    They excel in grounded reasoning, structured outputs, and on-device inference across a wide range of applications.
  </p>

  <div class="usecase-grid">

    <div class="usecase-card">
      <div class="usecase-title">In-Context Q&A (RAG)</div>
      <div class="usecase-desc">
        Grounded question answering over internal documents, knowledge bases, and proprietary datasets.
        Ideal for enterprise copilots, internal search, and knowledge assistants with hallucination-resistant responses.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Private / Local Q&A</div>
      <div class="usecase-desc">
        Fully on-device or on-prem AI assistants that keep sensitive data local.
        Well suited for healthcare, finance, legal, and compliance-heavy environments.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Text Extraction & Structured Outputs</div>
      <div class="usecase-desc">
        Reliable extraction of entities, fields, and structured JSON from documents, logs,
        forms, and unstructured text for automation and workflow pipelines.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Text Classification & Tagging</div>
      <div class="usecase-desc">
        Lightweight classification for moderation, intent detection, routing,
        and large-scale content processing with fast CPU inference.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Recommendations & Ranking</div>
      <div class="usecase-desc">
        Semantic retrieval, reranking, and scoring pipelines for feeds, search systems,
        and personalized user experiences with low-latency model inference.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">On-Device & Edge AI Applications</div>
      <div class="usecase-desc">
        Deploy AI directly in mobile apps, browsers, and edge environments for real-time UX,
        lower infrastructure costs, and improved privacy guarantees.
      </div>
    </div>

  </div>
</div>

<!-- WHY TEAPOT -->
<div class="section">
  <h2>Why Companies Choose TeapotAI</h2>
  <p>
    Unlike large API-only models, Teapot is built for efficient deployment. Models are optimized for
    speed, cost-efficiency, and privacy, making them ideal for production environments that require
    predictable latency and scalable inference.
  </p>

  <div class="usecase-grid">
    <div class="usecase-card">
      <div class="usecase-title">Ultra Low Latency</div>
      <div class="usecase-desc">
        Small, efficient architectures designed to run significantly faster than traditional large models,
        especially on CPU and edge devices.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Cost Efficient Inference</div>
      <div class="usecase-desc">
        Reduce or eliminate per-token API costs by running models locally or on lightweight infrastructure.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Privacy-First Deployment</div>
      <div class="usecase-desc">
        Keep enterprise and user data fully private with local, on-device, or on-prem model execution.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">Open Source + Enterprise Support</div>
      <div class="usecase-desc">
        Use Teapot models freely and partner with us for deployment, fine-tuning,
        hosting, evaluation, and long-term enterprise support.
      </div>
    </div>
  </div>
</div>

<!-- FINAL CTA -->
<div class="enterprise-cta">
  <h3>Deploy TeapotAI in Production</h3>
  <p>
    Tell us your use case, latency targets, and deployment environment (mobile, browser, CPU, or on-prem).
    We’ll help you design and deploy the optimal TeapotAI solution for your product.
  </p>
  <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
    Contact Sales — hello@teapotai.com
  </a>
</div>

</div>
