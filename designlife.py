<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나의 두 가지 인생 그래프</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- Chosen Palette: Warm Harmony -->
    <!-- Application Structure Plan: The application is designed as a guided, three-step interactive worksheet. Step 1 is the introduction. Step 2 presents two parallel chart areas for the 'Dream Path' and 'Realistic Path', allowing users to interactively plot their life graphs by clicking to add points representing life events and happiness levels. This side-by-side comparison structure was chosen to directly facilitate the core goal of the source worksheet: comparing two potential life paths based on different choices. Step 3 provides a text area for reflection. This linear, step-by-step flow is intuitive for the target audience (middle school students) and guides them through the creative and reflective process without overwhelming them. -->
    <!-- Visualization & Content Choices: 
    - Report Info: Life Graph 1 (Dream Path) -> Goal: Visualize a potential future based on passion. -> Viz Method: Interactive Line Chart (Chart.js/Canvas). -> Interaction: User clicks on the canvas to add data points (age, happiness), which dynamically draws their life curve. An associated list shows the events. -> Justification: An interactive chart is more engaging and personal than a static drawing, allowing students to 'own' their creation. Chart.js is lightweight and ideal for this.
    - Report Info: Life Graph 2 (Realistic Path) -> Goal: Visualize a potential future based on practical choices. -> Viz Method: Interactive Line Chart (Chart.js/Canvas). -> Interaction: Same click-to-add-point mechanism as Graph 1. -> Justification: Maintains consistency and allows for direct visual comparison with the Dream Path graph.
    - Report Info: 'Main Choices' & 'Reason for Selection' text -> Goal: Capture qualitative reflection. -> Presentation Method: HTML <textarea>. -> Interaction: Standard text input. -> Justification: Simple and effective for capturing user's thoughts as required by the worksheet. -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->
    <style>
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #FDFBF8;
            color: #4A4A4A;
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 40vh;
        }
        @media (min-width: 768px) {
            .chart-container {
                height: 350px;
            }
        }
        .instruction-box {
            background-color: #FFF8F0;
            border-left: 4px solid #FDBA74;
        }
    </style>
</head>
<body class="antialiased">
    <div class="container mx-auto p-4 sm:p-6 lg:p-8">
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-orange-500">나의 두 가지 인생 그래프</h1>
            <p class="mt-2 text-lg text-gray-600">선택에 따라 달라지는 나의 미래를 그려보아요.</p>
        </header>

        <main>
            <div class="instruction-box p-4 rounded-lg mb-8">
                <h2 class="text-xl font-bold text-orange-700 mb-2">🎨 사용 방법</h2>
                <p class="text-gray-700">
                    아래 두 개의 그래프는 여러분의 미래를 담는 캔버스입니다. <br>
                    1. 그래프의 원하는 지점(나이와 행복지수)을 클릭하여 인생의 중요한 순간을 점으로 표시하세요.<br>
                    2. 각 점은 선으로 연결되어 여러분만의 인생 곡선을 만들게 됩니다.<br>
                    3. '초기화' 버튼으로 언제든 다시 시작할 수 있어요.
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <h3 class="text-2xl font-bold text-center text-teal-600 mb-4">인생 그래프 1</h3>
                    <p class="text-center text-gray-500 mb-4 font-semibold">💖 내가 정말 원하는 선택을 했을 때</p>
                    <div class="chart-container">
                        <canvas id="lifeGraph1"></canvas>
                    </div>
                    <div class="mt-4 text-center">
                        <button id="resetGraph1" class="bg-teal-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-600 transition duration-300">그래프 초기화</button>
                    </div>
                     <div class="mt-6">
                        <label for="choices1" class="block text-lg font-semibold text-gray-700 mb-2">주요 선택들</label>
                        <textarea id="choices1" rows="4" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition" placeholder="이 미래를 만들기 위해 어떤 중요한 선택들을 했나요? (예: 좋아하는 동아리 활동에 집중하기, 예술 고등학교에 진학하기)"></textarea>
                    </div>
                </div>

                <div class="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
                    <h3 class="text-2xl font-bold text-center text-indigo-600 mb-4">인생 그래프 2</h3>
                    <p class="text-center text-gray-500 mb-4 font-semibold">🧭 또 다른 선택을 했을 때</p>
                    <div class="chart-container">
                        <canvas id="lifeGraph2"></canvas>
                    </div>
                    <div class="mt-4 text-center">
                        <button id="resetGraph2" class="bg-indigo-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-600 transition duration-300">그래프 초기화</button>
                    </div>
                    <div class="mt-6">
                        <label for="choices2" class="block text-lg font-semibold text-gray-700 mb-2">주요 선택들</label>
                        <textarea id="choices2" rows="4" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition" placeholder="이 미래를 만들기 위해 어떤 중요한 선택들을 했나요? (예: 성적에 맞춰 일반고에 진학하기, 안정적인 직업을 목표로 공부하기)"></textarea>
                    </div>
                </div>
            </div>

            <div class="mt-12 bg-white p-8 rounded-xl shadow-lg border border-gray-200">
                <h2 class="text-2xl font-bold text-center text-orange-500 mb-4">🤔 나의 자서전에 담을 그래프 선택하기</h2>
                <p class="text-center text-gray-600 mb-6">두 그래프를 비교해보고, 어떤 삶이 '가장 나다운 삶'이라고 생각되는지, 그 이유는 무엇인지 자유롭게 적어보세요.</p>
                <textarea id="reflection" rows="6" class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition" placeholder="어떤 인생 그래프가 더 마음에 와닿나요? 그 이유는 무엇인가요? 여러분의 생각을 들려주세요."></textarea>
            </div>
        </main>
        
        <footer class="text-center mt-12 py-4 border-t">
            <p class="text-gray-500">&copy; 2025 나의 미래 그리기 프로젝트. All rights reserved.</p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const createLifeGraph = (canvasId, borderColor, pointBackgroundColor) => {
                const ctx = document.getElementById(canvasId).getContext('2d');
                const data = {
                    labels: Array.from({ length: 14 }, (_, i) => (i * 5) + 15),
                    datasets: [{
                        label: '행복 지수',
                        data: [],
                        borderColor: borderColor,
                        backgroundColor: borderColor,
                        pointBackgroundColor: pointBackgroundColor,
                        pointBorderColor: '#ffffff',
                        pointHoverBackgroundColor: '#ffffff',
                        pointHoverBorderColor: pointBackgroundColor,
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        pointBorderWidth: 2,
                        tension: 0.3,
                        fill: false,
                        showLine: true
                    }]
                };

                const options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10,
                            title: {
                                display: true,
                                text: '행복 지수 / 만족도',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: '나이',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                title: function(context) {
                                    return `${context[0].label}세`;
                                },
                                label: function(context) {
                                    return `행복 지수: ${context.parsed.y}`;
                                }
                            }
                        }
                    },
                    onClick: (event, elements, chart) => {
                        const canvas = chart.canvas;
                        const rect = canvas.getBoundingClientRect();
                        const x = event.clientX - rect.left;
                        const y = event.clientY - rect.top;

                        const xValue = chart.scales.x.getValueForPixel(x);
                        const yValue = chart.scales.y.getValueForPixel(y);

                        const age = Math.round(data.labels[xValue]);
                        const happiness = Math.max(0, Math.min(10, yValue.toFixed(1)));

                        if (age !== undefined && happiness !== null) {
                            const dataset = chart.data.datasets[0];
                            dataset.data.push({ x: age, y: happiness });
                            dataset.data.sort((a, b) => a.x - b.x);
                            chart.update();
                        }
                    }
                };

                return new Chart(ctx, {
                    type: 'line',
                    data: data,
                    options: options
                });
            };

            const lifeGraph1 = createLifeGraph('lifeGraph1', 'rgba(20, 184, 166, 1)', 'rgba(13, 148, 136, 1)');
            const lifeGraph2 = createLifeGraph('lifeGraph2', 'rgba(99, 102, 241, 1)', 'rgba(79, 70, 229, 1)');

            document.getElementById('resetGraph1').addEventListener('click', () => {
                lifeGraph1.data.datasets[0].data = [];
                lifeGraph1.update();
            });

            document.getElementById('resetGraph2').addEventListener('click', () => {
                lifeGraph2.data.datasets[0].data = [];
                lifeGraph2.update();
            });
        });
    </script>
</body>
</html>
