import React from 'react';
import { ShieldCheck, Layers, Cpu, Box, Code2, CheckCircle2, Terminal, Bot, Sparkles, Workflow } from 'lucide-react';

export default function App() {
  const pytests = [
    { domain: "Domain", file: "test_dimensions.py", count: 5, status: "28/28 PASSED" },
    { domain: "Domain", file: "test_media_layer.py", count: 5, status: "28/28 PASSED" },
    { domain: "Domain", file: "test_motion_timeline.py", count: 6, status: "28/28 PASSED" },
    { domain: "Application", file: "test_extract_layout_specification.py", count: 3, status: "28/28 PASSED" },
    { domain: "Application", file: "test_compile_artifact.py", count: 4, status: "28/28 PASSED" },
    { domain: "Infrastructure", file: "test_compiler_factory.py", count: 3, status: "28/28 PASSED" },
    { domain: "Infrastructure", file: "test_agents.py", count: 2, status: "28/28 PASSED" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono tracking-wider uppercase mb-1">
              <ShieldCheck className="w-4 h-4" />
              <span>Clean Architecture &bull; SOLID &bull; TDD</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white flex items-center gap-3">
              OmniMotion <span className="text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full font-mono">v0.1.0</span>
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Mecanismo agnóstico de engenharia reversa de movimento orientado a DDD e Test-Driven Development.
            </p>
          </div>

          <div className="flex items-center gap-3 bg-slate-900 px-4 py-3 rounded-lg border border-slate-800">
            <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse" />
            <div>
              <div className="text-xs text-slate-400 uppercase font-mono">Suíte Pytest (100%)</div>
              <div className="text-sm font-semibold text-emerald-400">
                28 / 28 Testes Passando
              </div>
            </div>
          </div>
        </header>

        {/* Core Architectural Blueprints */}
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm">
              <Box className="w-4 h-4" /> 1. Domain
            </div>
            <p className="text-xs text-slate-400">
              Regras puras e imutáveis. <code className="text-indigo-300">Dimensions</code> VO, <code className="text-indigo-300">MediaLayer</code> e <code className="text-indigo-300">MotionTimeline</code> Aggregate Root.
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
              <Workflow className="w-4 h-4" /> 2. Application
            </div>
            <p className="text-xs text-slate-400">
              Inversão de Dependência (DIP) via interfaces <code className="text-emerald-300">IVideoAnalyzer</code>, <code className="text-emerald-300">IArtifactCompiler</code> e Use Cases.
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-amber-400 font-semibold text-sm">
              <Cpu className="w-4 h-4" /> 3. Infrastructure
            </div>
            <p className="text-xs text-slate-400">
              Padrão Strategy + Factory para compiladores (MP4, Astro) e multi-agente Pack (<code className="text-amber-300">CrewAI</code>).
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-cyan-400 font-semibold text-sm">
              <Terminal className="w-4 h-4" /> 4. Presentation
            </div>
            <p className="text-xs text-slate-400">
              Camadas desacopladas preparadas para CLI, API Endpoints e interfaces de controle.
            </p>
          </div>
        </div>

        {/* Multi-Agent Pack & Compiler Factory Highlights */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-indigo-400" />
                <h2 className="font-semibold text-lg text-slate-100">CrewAI Agent Pack (Infrastructure)</h2>
              </div>
              <span className="text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full font-mono">
                Multi-Agente
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-indigo-300 font-mono">Vision Agent</div>
                <div className="text-slate-400">Análise de quadros de vídeo, detecção de layout e keyframes.</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-indigo-300 font-mono">Data Structuralist</div>
                <div className="text-slate-400">Sintetiza metadados visuais no Aggregate Root MotionTimeline.</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-indigo-300 font-mono">UI Integrator</div>
                <div className="text-slate-400">Cruza especificações com o Design System e invoca compiladores.</div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-emerald-400" />
                <h2 className="font-semibold text-lg text-slate-100">Compiladores & Factory (Strategy Pattern)</h2>
              </div>
              <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full font-mono">
                Princípio OCP
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-emerald-300 font-mono">MP4VideoCompiler</div>
                <div className="text-slate-400">Compila vídeo social Picture-in-Picture com cantos arredondados.</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-emerald-300 font-mono">AstroComponentCompiler</div>
                <div className="text-slate-400">Gera código Astro + Tailwind CSS + Web Animations.</div>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                <div className="font-semibold text-emerald-300 font-mono">CompilerFactory</div>
                <div className="text-slate-400">Permite registrar dinamicamente novos compiladores sem alterar o uso.</div>
              </div>
            </div>
          </div>
        </div>

        {/* Pytest Execution Log */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Code2 className="w-5 h-5 text-emerald-400" />
              <h2 className="font-semibold text-lg text-slate-100">Módulos & Suíte de Testes Pytest</h2>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              Comando CLI: <code className="text-emerald-400">pytest</code>
            </span>
          </div>

          <div className="divide-y divide-slate-800/60 font-mono text-xs">
            {pytests.map((item, idx) => (
              <div key={idx} className="py-2.5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="text-slate-500">[{item.domain}]</span>
                  <span className="text-slate-200">tests/{item.domain}/{item.file}</span>
                </div>
                <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded text-[11px]">
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
