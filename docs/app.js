/**
 * AI in Games — Tic-Tac-Toe with Minimax AI
 * ==========================================
 * Browser-based implementation with real-time AI stats,
 * smooth animations, and particle background.
 * 
 * Author: Justin Sarosh Thomas
 */

// ─── PARTICLE BACKGROUND ───────────────────────────────────────
(function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 60;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.5 + 0.1;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(99, 102, 241, ${this.opacity})`;
            ctx.fill();
        }
    }

    for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());

    function connectParticles() {
        for (let a = 0; a < particles.length; a++) {
            for (let b = a + 1; b < particles.length; b++) {
                const dx = particles[a].x - particles[b].x;
                const dy = particles[a].y - particles[b].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 150) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(99, 102, 241, ${0.08 * (1 - dist / 150)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });
        connectParticles();
        requestAnimationFrame(animate);
    }
    animate();
})();

// ─── SMOOTH SCROLL NAV ─────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// Nav active state on scroll
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section');
window.addEventListener('scroll', () => {
    const nav = document.getElementById('main-nav');
    nav.classList.toggle('scrolled', window.scrollY > 50);
    let current = '';
    sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 200) current = s.getAttribute('id');
    });
    navLinks.forEach(l => {
        l.classList.toggle('active', l.getAttribute('href') === '#' + current);
    });
});

// ─── SCROLL REVEAL ANIMATIONS ──────────────────────────────────
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.algo-card, .feature-card, .pseudocode-block, .file-tree, .cta-block, .game-layout').forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
});

// ─── TIC-TAC-TOE GAME ENGINE ───────────────────────────────────
const WINNING_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

const WIN_LINE_POSITIONS = {
    '0,1,2': { x1: 10, y1: 16.7, x2: 90, y2: 16.7 },
    '3,4,5': { x1: 10, y1: 50, x2: 90, y2: 50 },
    '6,7,8': { x1: 10, y1: 83.3, x2: 90, y2: 83.3 },
    '0,3,6': { x1: 16.7, y1: 10, x2: 16.7, y2: 90 },
    '1,4,7': { x1: 50, y1: 10, x2: 50, y2: 90 },
    '2,5,8': { x1: 83.3, y1: 10, x2: 83.3, y2: 90 },
    '0,4,8': { x1: 10, y1: 10, x2: 90, y2: 90 },
    '2,4,6': { x1: 90, y1: 10, x2: 10, y2: 90 }
};

let board = Array(9).fill(null);
let humanPlayer = 'X';
let aiPlayer = 'O';
let gameActive = true;
let isAiTurn = false;
let scores = { X: 0, O: 0 };
let moveHistory = [];
let aiStats = { nodes: 0, pruned: 0, score: 0, time: 0 };

const cells = document.querySelectorAll('.cell');
const statusEl = document.getElementById('game-status');
const moveListEl = document.getElementById('move-list');

cells.forEach(cell => {
    cell.addEventListener('click', () => handleCellClick(parseInt(cell.dataset.index)));
});

document.getElementById('btn-reset').addEventListener('click', resetGame);
document.getElementById('btn-swap').addEventListener('click', swapSides);

function handleCellClick(index) {
    if (!gameActive || isAiTurn || board[index] !== null) return;
    makeMove(index, humanPlayer);
    if (!gameActive) return;
    isAiTurn = true;
    statusEl.textContent = 'AI is thinking...';
    statusEl.classList.add('thinking');
    setTimeout(() => {
        const start = performance.now();
        aiStats = { nodes: 0, pruned: 0, score: 0, time: 0 };
        const bestMove = getBestMove();
        aiStats.time = performance.now() - start;
        if (bestMove !== null) makeMove(bestMove, aiPlayer);
        updateAIStats();
        isAiTurn = false;
        statusEl.classList.remove('thinking');
        if (gameActive) statusEl.textContent = `Your turn — place ${humanPlayer}`;
    }, 300);
}

function makeMove(index, player) {
    board[index] = player;
    const cell = cells[index];
    cell.textContent = player;
    cell.classList.add(player === 'X' ? 'x' : 'o', 'placed');
    cell.disabled = true;

    moveHistory.push({ player, position: index + 1 });
    updateMoveHistory();

    const winCombo = checkWinner(board);
    if (winCombo) {
        gameActive = false;
        scores[player]++;
        updateScores();
        highlightWin(winCombo, player);
        statusEl.textContent = player === humanPlayer ? '🎉 You win!' : '🤖 AI wins!';
        statusEl.classList.add(player === humanPlayer ? 'win' : 'lose');
    } else if (board.every(c => c !== null)) {
        gameActive = false;
        statusEl.textContent = '🤝 Draw!';
        statusEl.classList.add('draw');
    }
}

function checkWinner(b) {
    for (const combo of WINNING_COMBOS) {
        const [a, c, d] = combo;
        if (b[a] && b[a] === b[c] && b[a] === b[d]) return combo;
    }
    return null;
}

function highlightWin(combo, player) {
    combo.forEach(i => cells[i].classList.add('winning'));
    const key = combo.join(',');
    const pos = WIN_LINE_POSITIONS[key];
    if (pos) {
        const line = document.getElementById('win-line');
        const color = player === 'X' ? '#6366f1' : '#f43f5e';
        line.style.cssText = `
            display: block;
            left: ${pos.x1}%; top: ${pos.y1}%;
            width: ${Math.sqrt((pos.x2-pos.x1)**2 + (pos.y2-pos.y1)**2)}%;
            transform: rotate(${Math.atan2(pos.y2-pos.y1, pos.x2-pos.x1)}rad);
            background: ${color};
            transform-origin: 0 50%;
            animation: winLineGrow 0.4s ease-out forwards;
        `;
    }
}

// ─── MINIMAX AI ─────────────────────────────────────────────────
function getBestMove() {
    let bestScore = -Infinity;
    let bestMove = null;
    const available = board.map((c, i) => c === null ? i : -1).filter(i => i >= 0);
    for (const move of available) {
        board[move] = aiPlayer;
        const score = minimax(board, 0, false, -Infinity, Infinity);
        board[move] = null;
        if (score > bestScore) { bestScore = score; bestMove = move; }
    }
    aiStats.score = bestScore;
    return bestMove;
}

function minimax(b, depth, isMax, alpha, beta) {
    aiStats.nodes++;
    const win = checkWinner(b);
    if (win) {
        const winner = b[win[0]];
        return winner === aiPlayer ? 10 - depth : -10 + depth;
    }
    if (b.every(c => c !== null)) return 0;

    if (isMax) {
        let maxEval = -Infinity;
        for (let i = 0; i < 9; i++) {
            if (b[i] !== null) continue;
            b[i] = aiPlayer;
            const eval_ = minimax(b, depth + 1, false, alpha, beta);
            b[i] = null;
            maxEval = Math.max(maxEval, eval_);
            alpha = Math.max(alpha, eval_);
            if (beta <= alpha) { aiStats.pruned++; break; }
        }
        return maxEval;
    } else {
        let minEval = Infinity;
        for (let i = 0; i < 9; i++) {
            if (b[i] !== null) continue;
            b[i] = humanPlayer;
            const eval_ = minimax(b, depth + 1, true, alpha, beta);
            b[i] = null;
            minEval = Math.min(minEval, eval_);
            beta = Math.min(beta, eval_);
            if (beta <= alpha) { aiStats.pruned++; break; }
        }
        return minEval;
    }
}

// ─── UI UPDATES ─────────────────────────────────────────────────
function updateAIStats() {
    document.getElementById('stat-nodes').textContent = aiStats.nodes.toLocaleString();
    document.getElementById('stat-pruned').textContent = aiStats.pruned.toLocaleString();
    document.getElementById('stat-score').textContent = aiStats.score > 0 ? `+${aiStats.score}` : aiStats.score.toString();
    document.getElementById('stat-time').textContent = `${aiStats.time.toFixed(1)}ms`;
}

function updateScores() {
    document.getElementById('score-x').textContent = scores.X;
    document.getElementById('score-o').textContent = scores.O;
}

function updateMoveHistory() {
    if (moveHistory.length === 0) {
        moveListEl.innerHTML = '<div class="move-empty">No moves yet</div>';
        return;
    }
    moveListEl.innerHTML = moveHistory.map((m, i) =>
        `<div class="move-item"><span class="move-num">${i + 1}.</span><span class="move-mark ${m.player === 'X' ? 'x' : 'o'}">${m.player}</span><span>→ Position ${m.position}</span></div>`
    ).join('');
    moveListEl.scrollTop = moveListEl.scrollHeight;
}

function resetGame() {
    board = Array(9).fill(null);
    gameActive = true;
    isAiTurn = false;
    moveHistory = [];
    cells.forEach(cell => {
        cell.textContent = '';
        cell.className = 'cell';
        cell.disabled = false;
    });
    document.getElementById('win-line').style.display = 'none';
    statusEl.className = 'game-status';
    updateMoveHistory();
    ['stat-nodes', 'stat-pruned', 'stat-score', 'stat-time'].forEach(id =>
        document.getElementById(id).textContent = '—'
    );

    if (humanPlayer === 'O') {
        isAiTurn = true;
        statusEl.textContent = 'AI is thinking...';
        setTimeout(() => {
            aiStats = { nodes: 0, pruned: 0, score: 0, time: 0 };
            const start = performance.now();
            const bestMove = getBestMove();
            aiStats.time = performance.now() - start;
            if (bestMove !== null) makeMove(bestMove, aiPlayer);
            updateAIStats();
            isAiTurn = false;
            statusEl.textContent = `Your turn — place ${humanPlayer}`;
        }, 300);
    } else {
        statusEl.textContent = `Your turn — place ${humanPlayer}`;
    }
}

function swapSides() {
    humanPlayer = humanPlayer === 'X' ? 'O' : 'X';
    aiPlayer = humanPlayer === 'X' ? 'O' : 'X';
    document.getElementById('player-x-name').textContent = humanPlayer === 'X' ? 'You' : 'AI';
    document.getElementById('player-o-name').textContent = humanPlayer === 'O' ? 'You' : 'AI';
    resetGame();
}

// ─── STAT COUNTER ANIMATION ────────────────────────────────────
function animateCounters() {
    document.querySelectorAll('.stat-value').forEach(el => {
        const text = el.textContent.trim();
        const num = parseInt(text.replace(/,/g, ''));
        if (isNaN(num) || num === 0) return;
        const duration = 2000;
        const start = performance.now();
        const original = el.textContent;
        function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(num * eased);
            el.textContent = current.toLocaleString();
            if (progress < 1) requestAnimationFrame(tick);
            else el.textContent = original;
        }
        requestAnimationFrame(tick);
    });
}

const heroObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) { animateCounters(); heroObserver.disconnect(); }
}, { threshold: 0.5 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObserver.observe(heroStats);
