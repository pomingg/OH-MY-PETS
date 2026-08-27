// ======================================
// 戰情中心 - 所有 14 個圖表集成代碼
// ======================================

// 辅助函数
function grid() {
  return { color: 'rgba(100,110,160,.15)', drawBorder: false };
}

// ================== 高優先級 ==================

// 1️⃣ Overview - 健康分數環形圖
function initHealthScoreRings() {
  const ringData = [
    { label: '銷售', score: 82, delta: '+3 較上季', up: true, color: '#E8A33D' },
    { label: '生產與庫存', score: 76, delta: '-2 較上季', up: false, color: '#35B0AE' },
    { label: '人力資源', score: 68, delta: '-5 較上季', up: false, color: '#9B84E8' },
    { label: '財務', score: 88, delta: '+4 較上季', up: true, color: '#4FBD84' },
  ];

  const ringRow = document.getElementById('healthRingRow');
  if (!ringRow) return;

  ringRow.innerHTML = '';
  ringData.forEach(d => {
    const r = 54, c = 2 * Math.PI * r, dash = (d.score / 100) * c;
    const wrap = document.createElement('div');
    wrap.className = 'ring-card';
    wrap.innerHTML = `
      <svg width="100" height="100" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="${r}" fill="none" stroke="#1C2346" stroke-width="10"/>
        <circle cx="60" cy="60" r="${r}" fill="none" stroke="${d.color}" stroke-width="10"
          stroke-linecap="round" stroke-dasharray="${dash} ${c}" transform="rotate(-90 60 60)"/>
        <text x="60" y="66" text-anchor="middle" font-family="IBM Plex Mono" font-size="26" font-weight="600" fill="#EEF0FA">${d.score}</text>
      </svg>
      <div>
        <div class="ring-label">${d.label}健康分數</div>
        <div class="ring-delta ${d.up ? 'up' : 'down'}">${d.up ? '▲' : '▼'} ${d.delta}</div>
      </div>`;
    ringRow.appendChild(wrap);
  });
}

// 2️⃣ Sales - BCG 矩陣氣泡圖 (最複雜，5顆星)
const bcgProducts = [
  { name: '多層貓跳台款', yoy: 22, share: 18, revenue: 1400, q: 'star', line: 'own', channel: 'ecom', returnRate: 2.8 },
  { name: '基礎貓抓板', yoy: 4, share: 15, revenue: 1150, q: 'cow', line: 'own', channel: 'retail', returnRate: 3.2 },
  { name: '附玩具貓抓板', yoy: 15, share: 9, revenue: 700, q: 'question', line: 'own', channel: 'ecom', returnRate: 4.5 },
  { name: '保暖寵物窩', yoy: -3, share: 11, revenue: 850, q: 'cow', line: 'own', channel: 'retail', returnRate: 12.4 },
  { name: '一般寵物窩', yoy: -8, share: 5, revenue: 380, q: 'dog', line: 'own', channel: 'retail', returnRate: 5.0 },
  { name: '狗狗睡床豪華款', yoy: 28, share: 14, revenue: 1200, q: 'star', line: 'own', channel: 'ecom', returnRate: 2.1 },
  { name: '狗狗睡床基礎款', yoy: 8, share: 12, revenue: 920, q: 'cow', line: 'own', channel: 'retail', returnRate: 4.8 },
  { name: '兔籠配件組', yoy: -12, share: 3, revenue: 200, q: 'dog', line: 'own', channel: 'retail', returnRate: 6.2 },
  { name: '小動物飼料盆', yoy: 6, share: 8, revenue: 600, q: 'question', line: 'own', channel: 'ecom', returnRate: 7.1 },
  { name: '寵物玩具套組', yoy: 32, share: 10, revenue: 800, q: 'star', line: 'own', channel: 'ecom', returnRate: 3.5 },
];

const qColor = { star: '#E8A33D', cow: '#4FBD84', question: '#35B0AE', dog: '#E1596B' };

const quadPlugin = {
  id: 'quadBg',
  afterDatasetsDraw(chart) {
    const { ctx, chartArea, scales } = chart;
    if (!chartArea) return;
    const xMid = scales.x.getPixelForValue(10);
    const yMid = scales.y.getPixelForValue(10);
    ctx.save();
    ctx.fillStyle = 'rgba(232,163,61,.05)';
    ctx.fillRect(xMid, chartArea.top, chartArea.right - xMid, yMid - chartArea.top);
    ctx.fillStyle = 'rgba(79,189,132,.05)';
    ctx.fillRect(chartArea.left, yMid, xMid - chartArea.left, chartArea.bottom - yMid);
    ctx.fillStyle = 'rgba(53,176,174,.05)';
    ctx.fillRect(xMid, yMid, chartArea.right - xMid, chartArea.bottom - yMid);
    ctx.fillStyle = 'rgba(225,89,107,.05)';
    ctx.fillRect(chartArea.left, chartArea.top, xMid - chartArea.left, yMid - chartArea.top);
    ctx.strokeStyle = '#262E58';
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(xMid, chartArea.top);
    ctx.lineTo(xMid, chartArea.bottom);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(chartArea.left, yMid);
    ctx.lineTo(chartArea.right, yMid);
    ctx.stroke();
    ctx.restore();
  }
};

function initBCGMatrix() {
  const canvas = document.getElementById('bcgChart');
  if (!canvas) return;

  if (window.charts && window.charts.bcgChart) {
    window.charts.bcgChart.destroy();
  }

  window.charts.bcgChart = new Chart(canvas, {
    type: 'bubble',
    data: {
      datasets: [{
        data: bcgProducts.map(p => ({ x: p.yoy, y: p.share, r: Math.sqrt(p.revenue) / 2.6, label: p.name })),
        backgroundColor: bcgProducts.map(p => qColor[p.q] + 'CC'),
        borderColor: bcgProducts.map(p => qColor[p.q]),
        borderWidth: 1.5,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const p = ctx.raw;
              return `${p.label}｜YoY ${p.x}%｜佔比 ${p.y}%`;
            }
          }
        }
      },
      scales: {
        x: { title: { display: true, text: '年增率 YoY (%)', font: { size: 11 } }, grid: grid(), min: -15, max: 38 },
        y: { title: { display: true, text: '營收佔比 (%)', font: { size: 11 } }, grid: grid(), min: 0, max: 22 }
      }
    },
    plugins: [quadPlugin]
  });
}

// 3️⃣ Sales - 退貨率分析
function initReturnRateChart() {
  const canvas = document.getElementById('returnRateChart');
  if (!canvas) return;

  if (window.charts && window.charts.returnRateChart) {
    window.charts.returnRateChart.destroy();
  }

  window.charts.returnRateChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: bcgProducts.map(p => p.name),
      datasets: [{
        data: bcgProducts.map(p => p.returnRate),
        backgroundColor: bcgProducts.map(p => p.returnRate > 8 ? '#E1596B' : '#35B0AE'),
        borderRadius: 4,
        maxBarThickness: 26,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: grid(), title: { display: true, text: '退貨率 (%)', font: { size: 11 } } },
        y: { grid: { display: false }, ticks: { font: { size: 9.5 } } }
      }
    }
  });
}

// 4️⃣ HR - 接班風險表
function initSuccessionRiskTable() {
  const tableHTML = `
    <div class="panel tall" style="padding: 0;">
      <div style="padding: 18px 20px 12px;">
        <h4 style="margin: 0 0 2px;">經理級人才接班風險評估</h4>
        <div class="cap">按部門梯隊比例與年齡分布識別風險等級</div>
      </div>
      <table style="width:100%; border-collapse: collapse; font-size: 13px;">
        <thead style="background: rgba(100,110,160,.1); border-bottom: 1px solid var(--border-soft);">
          <tr>
            <th style="padding: 10px 20px; text-align: left; color: var(--text-secondary); font-weight: 600;">部門</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">經理年齡</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">副理人數</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">梯隊比</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">風險等級</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">生產部</td>
            <td style="padding: 12px 20px; text-align: center;">54</td>
            <td style="padding: 12px 20px; text-align: center;">2</td>
            <td style="padding: 12px 20px; text-align: center;">1:2</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(225,89,107,.15); color: #E1596B; padding: 3px 8px; border-radius: 20px; font-weight: 600;">🔴 高風險</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">品保部</td>
            <td style="padding: 12px 20px; text-align: center;">48</td>
            <td style="padding: 12px 20px; text-align: center;">4</td>
            <td style="padding: 12px 20px; text-align: center;">1:4</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(232,163,61,.15); color: #E8A33D; padding: 3px 8px; border-radius: 20px; font-weight: 600;">🟠 中風險</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">供應鏈部</td>
            <td style="padding: 12px 20px; text-align: center;">52</td>
            <td style="padding: 12px 20px; text-align: center;">3</td>
            <td style="padding: 12px 20px; text-align: center;">1:3</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(232,163,61,.15); color: #E8A33D; padding: 3px 8px; border-radius: 20px; font-weight: 600;">🟠 中風險</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">業務部</td>
            <td style="padding: 12px 20px; text-align: center;">46</td>
            <td style="padding: 12px 20px; text-align: center;">5</td>
            <td style="padding: 12px 20px; text-align: center;">1:5</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(79,189,132,.15); color: #4FBD84; padding: 3px 8px; border-radius: 20px; font-weight: 600;">🟢 低風險</span></td>
          </tr>
          <tr>
            <td style="padding: 12px 20px;">研發部</td>
            <td style="padding: 12px 20px; text-align: center;">50</td>
            <td style="padding: 12px 20px; text-align: center;">6</td>
            <td style="padding: 12px 20px; text-align: center;">1:6</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(79,189,132,.15); color: #4FBD84; padding: 3px 8px; border-radius: 20px; font-weight: 600;">🟢 低風險</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  `;

  const container = document.getElementById('successionRiskContainer');
  if (container) {
    container.innerHTML = tableHTML;
  }
}

// ================== 中優先級 ==================

// 5️⃣ HR - 年齡結構分布
function initAgeDistributionChart() {
  const canvas = document.getElementById('ageDistributionChart');
  if (!canvas) return;

  const ageData = {
    labels: ['20-30', '30-40', '40-50', '50-60', '60+'],
    values: [45, 32, 68, 54, 12]
  };

  if (window.charts && window.charts.ageDistributionChart) {
    window.charts.ageDistributionChart.destroy();
  }

  window.charts.ageDistributionChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: ageData.labels,
      datasets: [{
        label: '人數',
        data: ageData.values,
        backgroundColor: '#9B84E8',
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: grid() },
        x: { grid: { display: false } }
      }
    }
  });
}

// 6️⃣ HR - 年資結構分布
function initTenureDistributionChart() {
  const canvas = document.getElementById('tenureDistributionChart');
  if (!canvas) return;

  const tenureData = {
    labels: ['0-2年', '2-5年', '5-10年', '10-15年', '15+年'],
    values: [38, 52, 61, 48, 12]
  };

  if (window.charts && window.charts.tenureDistributionChart) {
    window.charts.tenureDistributionChart.destroy();
  }

  window.charts.tenureDistributionChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: tenureData.labels,
      datasets: [{
        label: '人數',
        data: tenureData.values,
        backgroundColor: '#9B84E8',
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: grid() },
        x: { grid: { display: false } }
      }
    }
  });
}

// 7️⃣ HR - 職等結構分布
function initGradeDistributionChart() {
  const canvas = document.getElementById('gradeDistributionChart');
  if (!canvas) return;

  const gradeData = {
    labels: ['副理', '專員', '助理', '實習生'],
    values: [8, 35, 78, 12]
  };

  if (window.charts && window.charts.gradeDistributionChart) {
    window.charts.gradeDistributionChart.destroy();
  }

  window.charts.gradeDistributionChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: gradeData.labels,
      datasets: [{
        label: '人數',
        data: gradeData.values,
        backgroundColor: '#9B84E8',
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: grid() },
        x: { grid: { display: false } }
      }
    }
  });
}

// 8️⃣ Finance - P&L 結構圖
function initPLStructureChart() {
  const canvas = document.getElementById('plStructureChart');
  if (!canvas) return;

  const data = [2138, -1405, 733, -464, 269, 25, 294, -59, 235];
  const colors = data.map(d => d >= 0 ? '#4FBD84' : '#E1596B');

  if (window.charts && window.charts.plStructureChart) {
    window.charts.plStructureChart.destroy();
  }

  window.charts.plStructureChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: ['營收', '銷售成本', '毛利', '營運費用', '營業淨利', '非營業項目', '稅前淨利', '所得稅', '淨利'],
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: grid() },
        y: { grid: { display: false } }
      }
    }
  });
}

// 9️⃣ Finance - 資產負債表結構
function initBalanceSheetChart() {
  const canvas = document.getElementById('balanceSheetChart');
  if (!canvas) return;

  if (window.charts && window.charts.balanceSheetChart) {
    window.charts.balanceSheetChart.destroy();
  }

  window.charts.balanceSheetChart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['流動資產', '固定資產', '其他資產', '流動負債', '長期負債', '股東權益'],
      datasets: [{
        data: [1842, 1156, 312, 1234, 895, 1181],
        backgroundColor: ['#4FBD84', '#35B0AE', '#9B84E8', '#E8A33D', '#E1596B', '#C9A1E8']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } }
    }
  });
}

// 🔟 Finance - 現金流量圖
function initCashFlowChart() {
  const canvas = document.getElementById('cashFlowChart');
  if (!canvas) return;

  const data = [285, -156, -42, 512];
  const colors = data.map(d => d >= 0 ? '#4FBD84' : '#E1596B');

  if (window.charts && window.charts.cashFlowChart) {
    window.charts.cashFlowChart.destroy();
  }

  window.charts.cashFlowChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: ['營業活動', '投資活動', '融資活動', '期末現金'],
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: grid() },
        x: { grid: { display: false } }
      }
    }
  });
}

// 1️⃣1️⃣ Finance - 應收帳款老化分析
function initReceivablesAgingChart() {
  const canvas = document.getElementById('receivablesAgingChart');
  if (!canvas) return;

  if (window.charts && window.charts.receivablesAgingChart) {
    window.charts.receivablesAgingChart.destroy();
  }

  window.charts.receivablesAgingChart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['0-30天', '31-60天', '61-90天', '90天以上'],
      datasets: [{
        data: [520, 185, 95, 48],
        backgroundColor: ['#4FBD84', '#E8A33D', '#E1596B', '#9B84E8']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } }
    }
  });
}

// ================== 完善功能 ==================

// 1️⃣2️⃣ Production - OEE 趨勢圖
function initOEETrendChart() {
  const canvas = document.getElementById('oeeTrendDetailChart');
  if (!canvas) return;

  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const oeeA = [76, 74, 75, 78, 76, 79, 80, 78, 77, 76, 75, 73];
  const oeeB = [68, 66, 67, 70, 68, 71, 69, 68, 67, 66, 65, 62];
  const oeeC = [72, 70, 71, 74, 72, 75, 76, 74, 73, 72, 71, 69];

  if (window.charts && window.charts.oeeTrendDetailChart) {
    window.charts.oeeTrendDetailChart.destroy();
  }

  window.charts.oeeTrendDetailChart = new Chart(canvas, {
    type: 'line',
    data: {
      labels: months,
      datasets: [
        {
          label: 'A廠',
          data: oeeA,
          borderColor: '#4FBD84',
          backgroundColor: 'rgba(79,189,132,0.1)',
          borderWidth: 2,
          tension: 0.4
        },
        {
          label: 'B廠',
          data: oeeB,
          borderColor: '#E1596B',
          backgroundColor: 'rgba(225,89,107,0.1)',
          borderWidth: 2,
          tension: 0.4
        },
        {
          label: 'C廠',
          data: oeeC,
          borderColor: '#35B0AE',
          backgroundColor: 'rgba(53,176,174,0.1)',
          borderWidth: 2,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } },
      scales: {
        y: { grid: grid(), min: 60, max: 85 },
        x: { grid: { display: false } }
      }
    }
  });
}

// 1️⃣3️⃣ Production - 停機時間分析
function initDowntimeAnalysisChart() {
  const canvas = document.getElementById('downtimeAnalysisChart');
  if (!canvas) return;

  if (window.charts && window.charts.downtimeAnalysisChart) {
    window.charts.downtimeAnalysisChart.destroy();
  }

  window.charts.downtimeAnalysisChart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: ['計劃性維保', '換模停機', '缺料停機', '品質問題', '設備故障', '其他'],
      datasets: [{
        data: [285, 156, 142, 98, 72, 45],
        backgroundColor: '#E8A33D',
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: grid(), title: { display: true, text: '停機時數（小時）', font: { size: 11 } } },
        y: { grid: { display: false } }
      }
    }
  });
}

// 1️⃣4️⃣ Production - 庫存水位圖
function initInventoryLevelChart() {
  const canvas = document.getElementById('inventoryLevelChart');
  if (!canvas) return;

  const days = Array.from({ length: 30 }, (_, i) => `${i + 1}日`);
  const levels = [485, 492, 488, 495, 502, 498, 505, 512, 508, 515, 520, 518, 512, 508, 505, 510, 515, 520, 525, 520, 515, 510, 505, 510, 515, 520, 525, 530, 528, 525];

  if (window.charts && window.charts.inventoryLevelChart) {
    window.charts.inventoryLevelChart.destroy();
  }

  window.charts.inventoryLevelChart = new Chart(canvas, {
    type: 'line',
    data: {
      labels: days,
      datasets: [{
        label: '庫存金額（萬元）',
        data: levels,
        borderColor: '#35B0AE',
        backgroundColor: 'rgba(53,176,174,0.1)',
        fill: true,
        borderWidth: 2,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } },
      scales: {
        y: { grid: grid(), title: { display: true, text: '金額（萬元）', font: { size: 11 } } },
        x: { grid: { display: false } }
      }
    }
  });
}

// 1️⃣5️⃣ Production - 供應商績效表
function initSupplierPerformanceTable() {
  const tableHTML = `
    <div class="panel" style="padding: 0;">
      <div style="padding: 18px 20px 12px;">
        <h4 style="margin: 0 0 2px;">供應商績效評分</h4>
        <div class="cap">準時率、品質、回應速度綜合評分</div>
      </div>
      <table style="width:100%; border-collapse: collapse; font-size: 13px;">
        <thead style="background: rgba(100,110,160,.1); border-bottom: 1px solid var(--border-soft);">
          <tr>
            <th style="padding: 10px 20px; text-align: left; color: var(--text-secondary); font-weight: 600;">供應商名稱</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">準時率</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">品質評分</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">綜合評分</th>
            <th style="padding: 10px 20px; text-align: center; color: var(--text-secondary); font-weight: 600;">評級</th>
          </tr>
        </thead>
        <tbody>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">精準電子供應</td>
            <td style="padding: 12px 20px; text-align: center;">95%</td>
            <td style="padding: 12px 20px; text-align: center;">92</td>
            <td style="padding: 12px 20px; text-align: center; font-family: IBM Plex Mono; font-weight: 600; color: #4FBD84;">93.5</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(79,189,132,.15); color: #4FBD84; padding: 3px 8px; border-radius: 20px; font-weight: 600;">A級</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">宏大塑膠材料</td>
            <td style="padding: 12px 20px; text-align: center;">88%</td>
            <td style="padding: 12px 20px; text-align: center;">85</td>
            <td style="padding: 12px 20px; text-align: center; font-family: IBM Plex Mono; font-weight: 600; color: #E8A33D;">86.5</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(232,163,61,.15); color: #E8A33D; padding: 3px 8px; border-radius: 20px; font-weight: 600;">B級</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">優質包裝工業</td>
            <td style="padding: 12px 20px; text-align: center;">92%</td>
            <td style="padding: 12px 20px; text-align: center;">89</td>
            <td style="padding: 12px 20px; text-align: center; font-family: IBM Plex Mono; font-weight: 600; color: #4FBD84;">90.5</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(79,189,132,.15); color: #4FBD84; padding: 3px 8px; border-radius: 20px; font-weight: 600;">A級</span></td>
          </tr>
          <tr style="border-bottom: 1px solid var(--border-soft);">
            <td style="padding: 12px 20px;">創新機械製造</td>
            <td style="padding: 12px 20px; text-align: center;">78%</td>
            <td style="padding: 12px 20px; text-align: center;">76</td>
            <td style="padding: 12px 20px; text-align: center; font-family: IBM Plex Mono; font-weight: 600; color: #E1596B;">77</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(225,89,107,.15); color: #E1596B; padding: 3px 8px; border-radius: 20px; font-weight: 600;">C級</span></td>
          </tr>
          <tr>
            <td style="padding: 12px 20px;">環保水性漆料</td>
            <td style="padding: 12px 20px; text-align: center;">85%</td>
            <td style="padding: 12px 20px; text-align: center;">82</td>
            <td style="padding: 12px 20px; text-align: center; font-family: IBM Plex Mono; font-weight: 600; color: #E8A33D;">83.5</td>
            <td style="padding: 12px 20px; text-align: center;"><span style="background: rgba(232,163,61,.15); color: #E8A33D; padding: 3px 8px; border-radius: 20px; font-weight: 600;">B級</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  `;

  const container = document.getElementById('supplierPerformanceContainer');
  if (container) {
    container.innerHTML = tableHTML;
  }
}

// 初始化所有圖表 (在頁面加載完成後)
function initializeAllCharts() {
  // 只初始化當前活躍頁面的圖表
  // 其他頁面的圖表會在用戶切換時初始化
}

// 在頁面加載時初始化
document.addEventListener('DOMContentLoaded', () => {
  // 初始化 Overview 頁面的圖表（因為它預設是活躍的）
  setTimeout(() => {
    initHealthScoreRings();
  }, 300);
});
