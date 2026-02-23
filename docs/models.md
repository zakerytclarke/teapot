## Models
Teapot models are designed to run anywhere- from local CPUs and edge devices to production scale systems, while staying strong on general-purpose tasks like question answering, summarization, and information extraction. They’re optimized for fast, efficient, and grounded responses, making them a good fit when latency, cost, and reliability matter.

Whether you need a lightweight model for on-device inference or a larger model for higher accuracy, the Teapot family provides flexible options that excel at in-context reasoning and hallucination-resistant outputs. If you’re looking to fine-tune for your specific use case (proprietary data, domain workflows, custom formatting/refusals), get in contact with us to discuss custom training and deployment.

<style>
  .teapot-model-grid{
    display:grid;
    grid-template-columns:repeat(2, minmax(0, 1fr));
    gap:16px;
    margin: 12px 0 24px 0;
  }
  @media (max-width: 860px){
    .teapot-model-grid{ grid-template-columns: 1fr; }
  }

  .teapot-card{
    position:relative;
    border:1px solid rgba(127,127,127,.25);
    border-radius:16px;
    padding:18px 18px 16px 18px;
    background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,0));
    box-shadow: 0 8px 24px rgba(0,0,0,.08);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    overflow:hidden;
  }
  .teapot-card:hover{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 14px 40px rgba(0,0,0,.14);
    border-color: rgba(127,127,127,.45);
  }

  .teapot-card .toprow{
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    gap:12px;
    margin-bottom:10px;
  }
  .teapot-title{
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0;
    line-height:1.2;
  }
  .teapot-badge{
    font-size: .78rem;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(127,127,127,.25);
    background: rgba(127,127,127,.08);
    white-space: nowrap;
  }
  .teapot-meta{
    display:flex;
    flex-wrap:wrap;
    gap:8px 12px;
    margin: 10px 0 12px 0;
    font-size: .92rem;
    opacity: .95;
  }
  .teapot-meta b{ font-weight: 650; }

  .teapot-desc{
    margin: 0 0 14px 0;
    font-size: .95rem;
    line-height: 1.45;
    opacity: .95;
  }

  .teapot-stats{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 12px 0 14px 0;
  }
  .teapot-stat{
    border:1px solid rgba(127,127,127,.18);
    border-radius: 12px;
    padding: 10px 12px;
    background: rgba(127,127,127,.06);
  }
  .teapot-stat .label{
    font-size: .78rem;
    opacity: .75;
    margin-bottom: 4px;
  }
  .teapot-stat .value{
    font-size: 1.05rem;
    font-weight: 700;
  }

  .teapot-actions{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin-top: 4px;
  }
  .teapot-btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    padding: 9px 12px;
    border-radius: 12px;
    border:1px solid rgba(127,127,127,.25);
    text-decoration:none !important;
    font-weight: 650;
    font-size: .92rem;
    background: rgba(127,127,127,.08);
    transition: background .15s ease, transform .15s ease, border-color .15s ease;
  }
  .teapot-btn:hover{
    background: rgba(127,127,127,.14);
    border-color: rgba(127,127,127,.45);
    transform: translateY(-1px);
  }
  .teapot-subtle{
    font-size: .82rem;
    opacity: .7;
    margin-top: 10px;
  }
</style>

<div class="teapot-model-grid">

  <!-- TinyTeapot -->
  <div class="teapot-card">
    <div class="toprow">
      <h3 class="teapot-title">TinyTeapot 🫖</h3>
      <span class="teapot-badge">Edge / CPU-friendly</span>
    </div>

    <div class="teapot-meta">
      <span><b>Params:</b> 77M</span>
      <span><b>Speed:</b> ~40 tok/s (Colab CPU)</span>
    </div>

    <p class="teapot-desc">
      A lightweight grounded model designed for fast, low-latency inference while still performing strong
      <b>in-context Q&A</b> and <b>hallucination-resistant extraction</b> when given a document/passages to cite from.
    </p>

    <div class="teapot-stats">
      <div class="teapot-stat">
        <div class="label">Downloads (last 30 days)</div>
        <div class="value" id="tiny_downloads_30d">—</div>
      </div>
      <div class="teapot-stat">
        <div class="label">Downloads (all time)</div>
        <div class="value" id="tiny_downloads_all">—</div>
      </div>
    </div>

    <div class="teapot-actions">
      <a class="teapot-btn" href="https://huggingface.co/teapotai/tinyteapot" target="_blank" rel="noopener">
        Hugging Face ↗
      </a>
    </div>

    <div class="teapot-subtle">Best for: mobile/CPU demos, low-latency grounded answering.</div>
  </div>

  <!-- TeapotLLM -->
  <div class="teapot-card">
    <div class="toprow">
      <h3 class="teapot-title">TeapotLLM 🫖</h3>
      <span class="teapot-badge">Higher accuracy</span>
    </div>

    <div class="teapot-meta">
      <span><b>Params:</b> 0.8B</span>
      <span><b>Speed:</b> ~5 tok/s (Colab CPU)</span>
    </div>

    <p class="teapot-desc">
      The larger “previous work” in the Teapot family: stronger grounding and extraction fidelity for
      <b>context-faithful Q&A</b>, refusal behavior, and structured information extraction—at higher compute cost.
    </p>

    <div class="teapot-stats">
      <div class="teapot-stat">
        <div class="label">Downloads (last 30 days)</div>
        <div class="value" id="llm_downloads_30d">—</div>
      </div>
      <div class="teapot-stat">
        <div class="label">Downloads (all time)</div>
        <div class="value" id="llm_downloads_all">—</div>
      </div>
    </div>

    <div class="teapot-actions">
      <a class="teapot-btn" href="https://huggingface.co/teapotai/teapotllm" target="_blank" rel="noopener">
        Hugging Face ↗
      </a>
    </div>

    <div class="teapot-subtle">Best for: best-quality grounded extraction/Q&A (when latency is less critical).</div>
  </div>

</div>

<script>
  // Fetch HF stats (downloads last 30d + downloads all time) and populate the cards.
  // NOTE: Some GitHub Pages setups/themes may block cross-origin fetches; if so, values will stay as "—".

  const HF_ENDPOINTS = {
    tiny: "https://huggingface.co/api/models/teapotai/tinyteapot?expand[]=downloads&expand[]=downloadsAllTime",
    llm:  "https://huggingface.co/api/models/teapotai/teapotllm?expand[]=downloads&expand[]=downloadsAllTime"
  };

  const fmt = (n) => {
    if (typeof n !== "number") return "—";
    try { return new Intl.NumberFormat().format(n); } catch { return String(n); }
  };

  async function loadModelStats(url) {
    const r = await fetch(url, { headers: { "Accept": "application/json" } });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  }

  async function main() {
    try {
      const [tiny, llm] = await Promise.all([
        loadModelStats(HF_ENDPOINTS.tiny),
        loadModelStats(HF_ENDPOINTS.llm)
      ]);

      document.getElementById("tiny_downloads_30d").textContent = fmt(tiny.downloads);
      document.getElementById("tiny_downloads_all").textContent = fmt(tiny.downloadsAllTime);

      document.getElementById("llm_downloads_30d").textContent = fmt(llm.downloads);
      document.getElementById("llm_downloads_all").textContent = fmt(llm.downloadsAllTime);
    } catch (e) {
      console.warn("Failed to load Hugging Face download stats:", e);
    }
  }

  main();
</script>
