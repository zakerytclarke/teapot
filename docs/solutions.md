<style>
/* Wrapper */
.enterprise-wrap{
  max-width: 1100px;
  margin: 0 auto;
  padding: 30px 20px 60px;
  color: #1a1a1a;
}

/* Hero Card (light, clean) */
.enterprise-hero{
  background: #ffffff;
  border-radius: 24px;
  padding: 32px 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

/* Text Fix (KEY CHANGE) */
.kicker{
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #6b7280;
  margin-bottom: 10px;
  font-weight: 600;
}

.hero-title{
  font-size: 40px;
  margin: 0 0 12px 0;
  font-weight: 700;
  color: #111827; /* DARK instead of faded */
}

.hero-subtitle{
  font-size: 17px;
  line-height: 1.6;
  color: #374151; /* readable grey */
  max-width: 760px;
  margin-bottom: 24px;
}

/* Buttons */
.cta-row{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-primary{
  background: #111827;
  color: #ffffff !important;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s ease;
}

.btn-primary:hover{
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.btn-secondary{
  background: #f3f4f6;
  color: #111827;
  padding: 12px 18px;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
}

/* Section */
.section{
  margin-top: 42px;
}

.section h2{
  font-size: 26px;
  margin-bottom: 8px;
  color: #111827;
}

.section p{
  color: #4b5563;
  margin-bottom: 26px;
  max-width: 800px;
  font-size: 15px;
}

/* Use Case Grid (light cards like models page) */
.usecase-grid{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
}

.usecase-card{
  grid-column: span 6;
  background: #ffffff;
  border-radius: 20px;
  padding: 22px;
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.usecase-card:hover{
  transform: translateY(-3px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.18);
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

/* Big CTA */
.enterprise-cta{
  margin-top: 50px;
  background: #ffffff;
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.enterprise-cta h3{
  font-size: 28px;
  margin-bottom: 10px;
  color: #111827;
}

.enterprise-cta p{
  color: #4b5563;
  margin-bottom: 22px;
  font-size: 16px;
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
