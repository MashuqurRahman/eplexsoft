const NAV = [
    { key:"home", label:"Home", items:[
      { id:"dashboard", label:"Dashboard", href:"{% url 'pos_dashboard_url' %}" },
    ]},
    { key:"sales", label:"Sales Operations", items:[
      { id:"pos", label:"POS (Billing)", href:"#" },
      { id:"due-collection", label:"Due Collection", href:"#", improvised:true },
      { id:"refund", label:"Refund", href:"#", improvised:true },
      { id:"order-update", label:"Order Update", href:"#" },
      { id:"invoice-report", label:"Invoice Report", href:"#" },
    ]},
    { key:"inventory", label:"Inventory & Procurement", items:[
      { id:"supplier", label:"Supplier", href:"#" },
      { id:"purchase-order", label:"Purchase Order", href:"#", improvised:true },
      { id:"purchase-history", label:"Purchase History", href:"#" },
      { id:"grn", label:"GRN (Goods Received Note)", href:"#" },
      { id:"product-reconciliation", label:"Product Reconciliation", href:"#" },
      { id:"stock-transfer", label:"Stock Transfer", href:"#", improvised:true },
    ]},
    { key:"finance", label:"Finance", items:[
      { id:"expense-head", label:"Expense Head", href:"#", improvised:true },
      { id:"expense-entry", label:"Expense Entry", href:"#" },
      { id:"cash-bank-ledger", label:"Cash / Bank Ledger", href:"#", improvised:true },
      { id:"supplier-due-payment", label:"Supplier Due / Payment", href:"#", improvised:true },
    ]},
    { key:"master", label:"Master / Setup Data", items:[
      { id:"product-master", label:"Product Master", href:"#", improvised:true },
      { id:"customer-master", label:"Customer Master", href:"#", improvised:true },
      { id:"branch-setup", label:"Branch / Counter Setup", href:"#", improvised:true },
      { id:"user-management", label:"User Management", href:"#", improvised:true },
      { id:"permission-management", label:"Permission Management", href:"#", improvised:true },
    ]},
    { key:"reports", label:"Reports", items:[
      { id:"reports", label:"All Reports", href:"#" },
    ]},
  ];
 
  const active = "{% block active_nav_id %}dashboard{% endblock %}";
 
  function renderNav(filterText=''){
    const q = filterText.toLowerCase();
    const el = document.getElementById('navGroups');
    el.innerHTML = NAV.map((g, gi) => {
      const items = g.items.filter(it => !q || it.label.toLowerCase().includes(q));
      if(q && items.length===0) return '';
      return `
        <div class="group" data-g="${gi}">
          <button class="group-head" data-toggle="${gi}">
            <span class="label">${g.label}</span>
            <span class="chev">▾</span>
          </button>
          <div class="group-items">
            ${items.map(it => `
              <a class="navitem ${it.id===active?'active':''}" href="${it.href}">
                <span class="dot"></span>
                <span>${it.label}</span>
                ${it.improvised ? '<span class="imp-tag">◆ ADDED</span>' : ''}
              </a>
            `).join('')}
          </div>
        </div>`;
    }).join('');
 
    el.querySelectorAll('.group-head').forEach(btn => {
      btn.addEventListener('click', () => btn.parentElement.classList.toggle('collapsed'));
    });
  }
 
  document.getElementById('navSearch').addEventListener('input', e => renderNav(e.target.value));
 
  renderNav();