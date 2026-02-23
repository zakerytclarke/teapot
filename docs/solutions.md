# Looking for Enterprise Support?

<style>
.enterprise-wrap{
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 64px;
  color: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.enterprise-hero{
  background: #ffffff;
  border-radius: 28px;
  padding: 36px 32px;
  box-shadow: 0 25px 70px rgba(0,0,0,0.15);
}

.kicker{
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 12px;
}

.hero-title{
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 14px 0;
  color: #111827;
}

.hero-subtitle{
  font-size: 17px;
  line-height: 1.65;
  color: #374151;
  max-width: 780px;
  margin-bottom: 22px;
}

.hero-badges{
  font-size: 14px;
  color: #4b5563;
  margin-top: 12px;
}

.cta-row{
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.btn-primary{
  background: #111827;
  color: #ffffff !important;
  padding: 13px 22px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s ease;
}

.btn-primary:hover{
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.2);
}

.btn-secondary{
  background: #f3f4f6;
  color: #111827;
  padding: 13px 22px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
}

.section{
  margin-top: 50px;
}

.section h2{
  font-size: 28px;
  color: #111827;
  margin-bottom: 10px;
}

.section p{
  color: #4b5563;
  font-size: 16px;
  max-width: 820px;
  margin-bottom: 30px;
  line-height: 1.6;
}

.usecase-grid{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

.usecase-card{
  grid-column: span 6;
  background: #ffffff;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.12);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.usecase-card:hover{
  transform: translateY(-4px);
  box-shadow: 0 26px 60px rgba(0,0,0,0.18);
}

.usecase-title{
  font-size: 19px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 10px;
}

.usecase-desc{
  font-size: 15px;
  color: #4b5563;
  line-height: 1.65;
}

.enterprise-cta{
  margin-top: 64px;
  background: #ffffff;
  border-radius: 30px;
  padding: 40px 32px;
  text-align: center;
  box-shadow: 0 30px 80px rgba(0,0,0,0.16);
}

.enterprise-cta h3{
  font-size: 32px;
  color: #111827;
  margin-bottom: 12px;
}

.enterprise-cta p{
  font-size: 17px;
  color: #4b5563;
  margin-bottom: 26px;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 900px){
  .usecase-card{
    grid-column: span 12;
  }
  .hero-title{
    font-size: 34px;
  }
}
</style>

<div class="enterprise-wrap">

<div class="enterprise-hero">
  <div class="kicker">🫖 Open Source Models · 🤝 Enterprise Support</div>
  <div class="hero-title">Deploy Fast, Private AI with TeapotAI</div>
  <div class="hero-subtitle">
    TeapotAI helps organizations deploy ultra-low latency AI that runs locally on CPUs, mobile devices,
    and browsers. Our Teapot model family is optimized for privacy, cost efficiency, and real-world
    production workloads — without relying on expensive GPU infrastructure or external APIs.
  </div>

  <div class="cta-row">
    <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
      🚀 Contact Sales
    </a>
    <a class="btn-secondary" href="/models">
      🧠 View Models
    </a>
  </div>

  <div class="hero-badges">
    ⚡ Ultra Low Latency • 🔒 Privacy First • 💸 Cost Efficient • 🫖 Open Source
  </div>
</div>

<div class="section">
  <h2>✨ Enterprise Use Cases</h2>
  <p>
    Teapot models are built for real production environments where latency, privacy, and scalability matter.
    They excel in grounded reasoning, structured outputs, and efficient on-device inference.
  </p>

  <div class="usecase-grid">

    <div class="usecase-card">
      <div class="usecase-title">📚 In-Context Q&A (RAG)</div>
      <div class="usecase-desc">
        Grounded question answering over internal documents, knowledge bases, and proprietary datasets.
        Ideal for enterprise copilots, internal search tools, and knowledge assistants with hallucination-resistant outputs.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">🔒 Private / Local Q&A</div>
      <div class="usecase-desc">
        Fully on-device or on-prem AI assistants that keep sensitive data local.
        Perfect for healthcare, finance, legal, and compliance-sensitive environments.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">🧾 Text Extraction & Structured Outputs</div>
      <div class="usecase-desc">
        Reliable extraction of structured JSON, entities, and key fields from documents,
        forms, logs, and unstructured text for automation and workflow pipelines.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">🏷️ Text Classification & Tagging</div>
      <div class="usecase-desc">
        Fast, lightweight classification for moderation, intent detection, routing,
        and large-scale content processing with extremely low latency inference.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">📊 Recommendations & Ranking</div>
      <div class="usecase-desc">
        Semantic retrieval, reranking, and scoring pipelines for feeds, search systems,
        and personalized user experiences using efficient small models.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">📱 On-Device & Edge AI Applications</div>
      <div class="usecase-desc">
        Deploy AI directly in mobile apps, browsers, and edge environments for real-time UX,
        lower infrastructure costs, and fully private inference.
      </div>
    </div>

  </div>
</div>

<div class="section">
  <h2>🫖 Why Companies Choose TeapotAI</h2>
  <p>
    Unlike large API-only models, Teapot is designed for efficient deployment at scale.
    Our models prioritize speed, privacy, and cost control while maintaining strong grounded reasoning performance.
  </p>

  <div class="usecase-grid">
    <div class="usecase-card">
      <div class="usecase-title">⚡ Ultra Low Latency</div>
      <div class="usecase-desc">
        Optimized small models that run significantly faster than traditional large LLMs,
        especially on CPU, browser, and edge environments.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">💸 Cost Efficient Inference</div>
      <div class="usecase-desc">
        Reduce or eliminate per-token API costs by running models locally or on lightweight infrastructure.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">🔐 Privacy-First Architecture</div>
      <div class="usecase-desc">
        Keep enterprise and user data fully private with local, on-device,
        or on-prem model execution.
      </div>
    </div>

    <div class="usecase-card">
      <div class="usecase-title">🧩 Open Source + Enterprise Support</div>
      <div class="usecase-desc">
        Use Teapot models for free and partner with us for deployment, fine-tuning,
        hosting, evaluation, and long-term enterprise support.
      </div>
    </div>
  </div>
</div>

<div class="enterprise-cta">
  <h3>🚀 Deploy TeapotAI in Production</h3>
  <p>
    Tell us your use case, latency requirements, and deployment environment (mobile, browser,
    CPU, or on-prem). We’ll help design and deploy the optimal TeapotAI solution for your product.
  </p>
  <a class="btn-primary" href="mailto:hello@teapotai.com?subject=TeapotAI Enterprise Inquiry">
    📩 Contact Sales — hello@teapotai.com
  </a>
</div>

</div>
