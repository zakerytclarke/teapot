<style>
:root{
  --bg: #0e1116;
  --card: #151a22;
  --card-soft: #1b2230;
  --border: rgba(255,255,255,0.08);
  --text: #e6eaf2;
  --muted: #a8b0c0;
  --accent: #ffffff;
  --cta: #ffffff;
  --cta-text: #0e1116;
}

/* Page Container */
.enterprise-wrap{
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 64px;
  color: var(--text);
}

/* Hero */
.enterprise-hero{
  background: linear-gradient(180deg, #161c26, #121720);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}

.kicker{
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.14em;
  color: var(--muted);
  margin-bottom: 12px;
}

.hero-title{
  font-size: 40px;
  margin: 0 0 12px 0;
  font-weight: 700;
}

.hero-subtitle{
  font-size: 17px;
  line-height: 1.6;
  color: var(--muted);
  max-width: 780px;
  margin-bottom: 24px;
}

/* CTA Buttons */
.cta-row{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-primary{
  background: var(--cta);
  color: var(--cta-text) !important;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  border: none;
}

.btn-secondary{
  background: transparent;
  color: var(--text);
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid var(--border);
}

/* Section */
.section{
  margin-top: 42px;
}

.section h2{
  font-size: 24px;
  margin-bottom: 8px;
}

.section p{
  color: var(--muted);
  margin-bottom: 24px;
  max-width: 800px;
}

/* Use Case Banners (Model-card style) */
.usecase-grid{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
}

.usecase-card{
  grid-column: span 6;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 22px 20px;
  transition: transform 0.15s ease, border 0.15s ease;
}

.usecase-card:hover{
  transform: translateY(-2px);
  border-color: rgba(255,255,255,0.18);
}

.usecase-title{
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
}

.usecase-desc{
  font-size: 14px;
  color: var(--muted);
  line-height: 1.6;
}

/* Big CTA Footer */
.enterprise-cta{
  margin-top: 50px;
  background: linear-gradient(180deg, #171e29, #111722);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
  text-align: center;
}

.enterprise-cta h3{
  font-size: 26px;
  margin-bottom: 10px;
}

.enterprise-cta p{
  color: var(--muted);
  margin-bottom: 22px;
  font-size: 15px;
}

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
    <h1 class="hero-title">Enterprise TeapotAI</h1>
    <p class="hero-subtitle">
      TeapotAI helps organizations deploy ultra-low latency AI that runs locally on CPUs, mobile devices, and browsers.
      Our Teapot model family is optimized for private, cost-efficient, and production-grade inference — without relying
      on expensive cloud APIs or large GPU infrastructure.
    </p>

    <div class="cta-row">
      <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
        Contact Sales
      </a>
      <a class="btn-secondary" href="/models">
        View Models
      </a>
    </div>
  </div>

  <!-- WHAT WE DO -->
  <div class="section">
    <h2>Enterprise Use Cases</h2>
    <p>
      Teapot models are designed for real production systems where latency, privacy, and cost constraints matter.
      Below are common high-impact deployments across startups and large organizations.
    </p>

    <div class="usecase-grid">

      <div class="usecase-card">
        <div class="usecase-title">📚 In-Context Q&A (RAG)</div>
        <div class="usecase-desc">
          Grounded question answering over internal documents, knowledge bases, and proprietary datasets.
          Ideal for enterprise copilots, internal assistants, and documentation search with hallucination-resistant outputs.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">🔒 Local / Private Q&A</div>
        <div class="usecase-desc">
          Fully on-device or on-prem AI assistants that never send sensitive data to external APIs.
          Perfect for healthcare, finance, and compliance-heavy environments.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">🧾 Text Extraction & Structured Outputs</div>
        <div class="usecase-desc">
          Reliable extraction of structured data (JSON) from documents, forms, logs, and unstructured text.
          Used for automation pipelines, document intelligence, and workflow tooling.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">🏷️ Text Classification</div>
        <div class="usecase-desc">
          Fast, lightweight classification models for tagging, moderation, intent detection,
          and large-scale content processing with low latency.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">📊 Recommendations & Ranking</div>
        <div class="usecase-desc">
          Re-ranking, retrieval scoring, and semantic matching for search systems,
          feeds, and personalized experiences where inference speed is critical.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">⚡ On-Device & Edge AI Applications</div>
        <div class="usecase-desc">
          Deploy AI directly on mobile apps, browsers, and edge environments.
          Enables real-time UX with near-zero latency and significantly lower infrastructure costs.
        </div>
      </div>

    </div>
  </div>

  <!-- WHY TEAPOT -->
  <div class="section">
    <h2>Why Companies Choose TeapotAI</h2>
    <p>
      Unlike large API-only models, Teapot is built for efficient, production-ready deployment.
      Models can run locally, scale cheaply, and provide predictable latency for real-world products.
    </p>

    <div class="usecase-grid">
      <div class="usecase-card">
        <div class="usecase-title">🚀 Ultra Low Latency</div>
        <div class="usecase-desc">
          Optimized small models that respond significantly faster than large LLMs,
          especially on CPU and edge environments.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">💸 Cost Efficient Inference</div>
        <div class="usecase-desc">
          Reduce or eliminate per-token API costs by running models locally or on lightweight infrastructure.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">🔐 Privacy First Architecture</div>
        <div class="usecase-desc">
          Keep user and enterprise data fully private with on-device and on-prem deployments.
        </div>
      </div>

      <div class="usecase-card">
        <div class="usecase-title">🫖 Open Source + Enterprise Support</div>
        <div class="usecase-desc">
          Use Teapot models for free. Work with us when you need deployment, fine-tuning,
          hosting, evaluation, or long-term support.
        </div>
      </div>
    </div>
  </div>

  <!-- BIG CTA -->
  <div class="enterprise-cta">
    <h3>Deploy TeapotAI in Production</h3>
    <p>
      Tell us your use case, latency requirements, and deployment environment (mobile, browser, CPU, or on-prem).
      We’ll recommend the optimal architecture and model setup for your product.
    </p>
    <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
      Contact Sales — hello@teapotai.com
    </a>
  </div>

</div>
