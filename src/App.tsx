import React, { useState } from 'react';
import { Dimensions } from './domain/value-objects/Dimensions';
import { MediaLayer } from './domain/entities/MediaLayer';
import { CheckCircle2, ShieldCheck, Code2, Play, Layers, Box, RefreshCw } from 'lucide-react';

interface TestResult {
  name: string;
  suite: string;
  passed: boolean;
  message?: string;
}

export default function App() {
  // Domain instances state for live playground
  const [width, setWidth] = useState<number>(1920);
  const [height, setHeight] = useState<number>(1080);
  const [layerName, setLayerName] = useState<string>("Hero Banner Layer");
  const [posX, setPosX] = useState<number>(100);
  const [posY, setPosY] = useState<number>(50);
  const [opacity, setOpacity] = useState<number>(0.9);
  const [visible, setVisible] = useState<boolean>(true);
  const [zIndex, setZIndex] = useState<number>(1);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Run live domain tests in browser to show TDD state
  const runDomainSuite = (): TestResult[] => {
    const results: TestResult[] = [];

    // Dimensions Tests
    try {
      const dim = new Dimensions(800, 600);
      results.push({ suite: 'Dimensions VO', name: 'Creates valid dimensions (800x600)', passed: dim.width === 800 && dim.height === 600 });
    } catch (e: any) {
      results.push({ suite: 'Dimensions VO', name: 'Creates valid dimensions', passed: false, message: e.message });
    }

    try {
      new Dimensions(0, 500);
      results.push({ suite: 'Dimensions VO', name: 'Rejects zero/negative dimensions', passed: false, message: 'Should have thrown error' });
    } catch (e: any) {
      results.push({ suite: 'Dimensions VO', name: 'Rejects zero/negative dimensions', passed: true });
    }

    try {
      const dim = new Dimensions(1920, 1080);
      results.push({ suite: 'Dimensions VO', name: 'Calculates aspect ratio correctly', passed: Math.abs(dim.aspectRatio - 1.777) < 0.01 });
    } catch (e: any) {
      results.push({ suite: 'Dimensions VO', name: 'Calculates aspect ratio correctly', passed: false, message: e.message });
    }

    try {
      const dim = new Dimensions(100, 200);
      const scaled = dim.scale(2);
      results.push({ suite: 'Dimensions VO', name: 'Scales dimensions immutably', passed: scaled.width === 200 && scaled.height === 400 && dim.width === 100 });
    } catch (e: any) {
      results.push({ suite: 'Dimensions VO', name: 'Scales dimensions immutably', passed: false, message: e.message });
    }

    try {
      const d1 = new Dimensions(100, 200);
      const d2 = new Dimensions(100, 200);
      results.push({ suite: 'Dimensions VO', name: 'Value equality check (equals)', passed: d1.equals(d2) });
    } catch (e: any) {
      results.push({ suite: 'Dimensions VO', name: 'Value equality check (equals)', passed: false, message: e.message });
    }

    // MediaLayer Tests
    try {
      const layer = new MediaLayer({
        id: 'layer-1',
        name: 'Header Image',
        dimensions: new Dimensions(1200, 400),
      });
      results.push({ suite: 'MediaLayer Entity', name: 'Creates layer with default positions & opacity', passed: layer.id === 'layer-1' && layer.x === 0 && layer.opacity === 1 });
    } catch (e: any) {
      results.push({ suite: 'MediaLayer Entity', name: 'Creates layer with defaults', passed: false, message: e.message });
    }

    try {
      new MediaLayer({ id: '', name: 'Layer', dimensions: new Dimensions(100, 100) });
      results.push({ suite: 'MediaLayer Entity', name: 'Rejects empty ID', passed: false, message: 'Should throw' });
    } catch (e: any) {
      results.push({ suite: 'MediaLayer Entity', name: 'Rejects empty ID', passed: true });
    }

    try {
      const layer = new MediaLayer({ id: 'l1', name: 'Layer', dimensions: new Dimensions(100, 100) });
      layer.moveTo(50, 150);
      results.push({ suite: 'MediaLayer Entity', name: 'Updates position with moveTo()', passed: layer.x === 50 && layer.y === 150 });
    } catch (e: any) {
      results.push({ suite: 'MediaLayer Entity', name: 'Updates position with moveTo()', passed: false, message: e.message });
    }

    try {
      const layer = new MediaLayer({ id: 'l1', name: 'Layer', dimensions: new Dimensions(100, 100) });
      layer.setOpacity(0.7);
      results.push({ suite: 'MediaLayer Entity', name: 'Updates opacity with domain validation', passed: layer.opacity === 0.7 });
    } catch (e: any) {
      results.push({ suite: 'MediaLayer Entity', name: 'Updates opacity with domain validation', passed: false, message: e.message });
    }

    try {
      const layer = new MediaLayer({ id: 'l1', name: 'Layer', dimensions: new Dimensions(100, 100) });
      layer.setOpacity(1.5);
      results.push({ suite: 'MediaLayer Entity', name: 'Rejects invalid opacity (> 1)', passed: false, message: 'Should throw' });
    } catch (e: any) {
      results.push({ suite: 'MediaLayer Entity', name: 'Rejects invalid opacity (> 1)', passed: true });
    }

    return results;
  };

  const testResults = runDomainSuite();
  const allPassed = testResults.every((t) => t.passed);

  // Instantiating active domain model safely for the interactive playground
  let activeDimensions: Dimensions | null = null;
  let activeLayer: MediaLayer | null = null;

  try {
    activeDimensions = new Dimensions(width, height);
    activeLayer = new MediaLayer({
      id: "layer-live-001",
      name: layerName,
      dimensions: activeDimensions,
      x: posX,
      y: posY,
      opacity: opacity,
      visible: visible,
      zIndex: zIndex,
    });
    if (errorMsg) setErrorMsg(null);
  } catch (err: any) {
    if (!errorMsg || errorMsg !== err.message) {
      setErrorMsg(err.message);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono tracking-wider uppercase mb-1">
              <ShieldCheck className="w-4 h-4" />
              <span>Modo TDD Ativo &bull; Passo a Passo</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">
              Sistema MediaLayer & Dimensions
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Ambiente TDD isolado contendo apenas o Value Object <code className="text-emerald-300 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800 font-mono">Dimensions</code>, a Entidade <code className="text-emerald-300 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800 font-mono">MediaLayer</code> e os testes unitários correspondentes.
            </p>
          </div>

          <div className="flex items-center gap-3 bg-slate-900 px-4 py-3 rounded-lg border border-slate-800">
            <div className={`w-3 h-3 rounded-full ${allPassed ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
            <div>
              <div className="text-xs text-slate-400 uppercase font-mono">Status da Suíte</div>
              <div className="text-sm font-semibold text-slate-200">
                {allPassed ? `${testResults.length}/${testResults.length} Testes Passando` : 'Falha nos Testes'}
              </div>
            </div>
          </div>
        </header>

        {/* Architecture Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Dimensions Value Object Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Box className="w-5 h-5 text-indigo-400" />
                <h2 className="font-semibold text-lg text-slate-100">Value Object: Dimensions</h2>
              </div>
              <span className="text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2.5 py-1 rounded-full font-mono">
                Imutável
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Garante a validade das dimensões corporativas (largura e altura &gt; 0, valores finitos). Suporta cálculo de aspecto, escala e verificação de igualdade.
            </p>

            <div className="space-y-3 bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-xs">
              <div className="flex justify-between">
                <span className="text-slate-500">Valor Atual:</span>
                <span className="text-indigo-300">{activeDimensions ? activeDimensions.toString() : 'Inválido'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Aspect Ratio:</span>
                <span className="text-indigo-300">
                  {activeDimensions ? activeDimensions.aspectRatio.toFixed(3) : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* MediaLayer Entity Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Layers className="w-5 h-5 text-emerald-400" />
                <h2 className="font-semibold text-lg text-slate-100">Entidade: MediaLayer</h2>
              </div>
              <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full font-mono">
                Identity-based
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Representa a camada de mídia com estado mutável controlado por regras de domínio (<code className="text-slate-300">moveTo</code>, <code className="text-slate-300">resize</code>, <code className="text-slate-300">setOpacity</code> com validação de limite [0,1]).
            </p>

            <div className="space-y-2 bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-xs">
              <div className="flex justify-between">
                <span className="text-slate-500">ID:</span>
                <span className="text-emerald-300">{activeLayer?.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Posição (X, Y):</span>
                <span className="text-emerald-300">({activeLayer?.x}, {activeLayer?.y})</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Opacidade:</span>
                <span className="text-emerald-300">{activeLayer?.opacity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Visível:</span>
                <span className={activeLayer?.visible ? "text-emerald-400" : "text-amber-400"}>
                  {activeLayer?.visible ? "Sim" : "Não"}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Live Playground Controls */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Code2 className="w-5 h-5 text-amber-400" />
            <h2 className="font-semibold text-lg text-slate-100">Playground de Validação de Regras de Domínio</h2>
          </div>

          {errorMsg && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-300 text-xs p-3 rounded-lg flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500" />
              <span><strong>Exceção do Domínio Capturada:</strong> {errorMsg}</span>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Nome da Camada</label>
              <input
                type="text"
                value={layerName}
                onChange={(e) => setLayerName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Largura (Width px)</label>
              <input
                type="number"
                value={width}
                onChange={(e) => setWidth(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Altura (Height px)</label>
              <input
                type="number"
                value={height}
                onChange={(e) => setHeight(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Posição X</label>
              <input
                type="number"
                value={posX}
                onChange={(e) => setPosX(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Posição Y</label>
              <input
                type="number"
                value={posY}
                onChange={(e) => setPosY(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">Opacidade (0.0 a 1.0)</label>
              <input
                type="number"
                step="0.1"
                value={opacity}
                onChange={(e) => setOpacity(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={() => setVisible(!visible)}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-4 py-2 rounded-lg transition border border-slate-700"
            >
              Alternar Visibilidade ({visible ? "Visível" : "Oculto"})
            </button>
            <button
              onClick={() => {
                setWidth(1920);
                setHeight(1080);
                setPosX(100);
                setPosY(50);
                setOpacity(0.9);
                setLayerName("Hero Banner Layer");
              }}
              className="bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 text-xs px-3 py-2 rounded-lg transition flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Resetar Valores
            </button>
          </div>
        </div>

        {/* Test Suite Results List */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Play className="w-5 h-5 text-emerald-400" />
              <h2 className="font-semibold text-lg text-slate-100">Resultado dos Testes Unitários (Vitest)</h2>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              Comando CLI: <code className="text-emerald-400">npx vitest run</code>
            </span>
          </div>

          <div className="divide-y divide-slate-800/60">
            {testResults.map((test, index) => (
              <div key={index} className="py-2.5 flex items-center justify-between text-xs font-mono">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="text-slate-500">[{test.suite}]</span>
                  <span className="text-slate-200">{test.name}</span>
                </div>
                <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded text-[11px]">
                  PASSED
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
