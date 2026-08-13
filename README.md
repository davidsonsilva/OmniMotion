# OmniMotion 🚀

**OmniMotion** é uma engine agnóstica e inteligente de **engenharia reversa de motion design e análise computacional de vídeo**. Utilizando uma arquitetura de múltiplos agentes (**CrewAI**) e os princípios de **Clean Architecture**, o sistema analisa gravações de tela e vídeos de interfaces, isola camadas visuais (backgrounds, overlays, janelas flutuantes, webcams), rastreia keyframes cinéticos em milissegundos e sintetiza essas informações em especificações estruturadas de movimento e código compilável (Astro, MP4, etc.).

---

## 🏛️ Arquitetura do Sistema (Clean Architecture)

O projeto segue estritamente os princípios da Clean Architecture, garantindo desacoplamento total entre as regras de negócio do domínio e as ferramentas de infraestrutura (LLMs, CrewAI, compilers):

```text
OmniMotion/
├── src/
│   ├── Domain/                      # Regras de Negócio Enterprise (Sem dependências externas)
│   │   ├── Entities/                # MotionTimeline, MediaLayer, Keyframe
│   │   └── ValueObjects/            # Dimensions
│   ├── Application/                 # Casos de Uso & Interfaces da Aplicação
│   │   ├── Interfaces/              # IVideoAnalyzer, IArtifactCompiler
│   │   └── UseCases/                # ExtractLayoutSpecificationUseCase, CompileArtifactUseCase
│   ├── Infrastructure/              # Implementações de Infraestrutura & Agentes AI
│   │   ├── Agents/                  # CrewAIVideoAnalyzer, MotionAgentPack
│   │   └── Compilers/               # AstroCompiler, MP4Compiler, CompilerFactory
│   └── Presentation/                # Interfaces de Entrada do Usuário
│       └── CLI/                     # main.py (Ponto de entrada de linha de comando)
└── tests/                           # Suíte de testes automatizados Pytest (38/38 passing)
```

---

## 🤖 Agentes Especialistas CrewAI

A análise de vídeo é orquestrada por uma equipe especialista (*Crew*) composta por dois agentes de IA com prompts e responsabilidades cirúrgicas:

### 1. 👁️ Vision Agent (`Analista Sênior de Motion Design e Visão Computacional`)
- **Papel**: Analista Sênior de Motion Design e Visão Computacional
- **Objetivo**: Analisar os frames do vídeo fornecido e extrair com precisão matemática a física, a estrutura de camadas e a linha do tempo do movimento.
- **Prompt Interno**: Engenheiro especialista em engenharia reversa visual. Rastreia camadas sobrepostas (como overlays de webcam/Picture-in-Picture), captura cantos arredondados (`border-radius`), opacidade e tempos exatos em milissegundos de cada animação, estimando curvas Bézier (`cubic-bezier`).

### 2. 📐 Data Structuralist (`Arquiteto de Design System e Engenheiro de Dados`)
- **Papel**: Arquiteto de Design System e Engenheiro de Dados
- **Objetivo**: Traduzir a análise bruta de movimento do Vision Agent em um esquema estruturado Pydantic que alimentará a entidade `MotionTimeline`.
- **Prompt Interno**: Especialista obcecado por padronização e tokens de design. Envolopa os metadados brutos estritamente nas classes Pydantic (`MediaLayerSchema`, `KeyframeSchema`, `MotionTimelineSchema`) garantindo um JSON final limpo e validado.

---

## 💻 Execução via Linha de Comando (CLI)

Você pode executar o pipeline completo de engenharia reversa diretamente do terminal apontando para qualquer vídeo de entrada:

```bash
# Configurar a chave da API do Gemini
export GEMINI_API_KEY="sua_chave_aqui"

# Executar a análise no arquivo de vídeo
python3 src/Presentation/CLI/main.py --video "caminho/para/seu_video.mp4"
```

---

## 📊 Exemplo Prático de Saída (JSON Especificação de Movimento)

Resultado extraído da execução do comando CLI para análise de layout e linha do tempo de movimento:

```json
{
  "timeline_id": "tl_omnimotion_input.mp4",
  "name": "Analysis of omnimotion_input.mp4",
  "duration_ms": 10000,
  "delay_ms": 0,
  "keyframes": [
    {
      "time_ms": 0,
      "properties": {
        "x": 0.0,
        "y": 0.0,
        "scale": 1.0
      },
      "easing": "cubic-bezier(0.25, 0.1, 0.25, 1.0)"
    },
    {
      "time_ms": 5000,
      "properties": {
        "x": 100.0,
        "y": 50.0,
        "scale": 1.2
      },
      "easing": "cubic-bezier(0.25, 0.1, 0.25, 1.0)"
    }
  ],
  "layers": [
    {
      "layer_id": "layer_screen",
      "name": "Screen Recording",
      "x": 0.0,
      "y": 0.0,
      "width": 1920.0,
      "height": 1080.0,
      "z_index": 0,
      "visible": true,
      "opacity": 1.0
    },
    {
      "layer_id": "layer_webcam",
      "name": "Webcam Overlay",
      "x": 1560.0,
      "y": 800.0,
      "width": 320.0,
      "height": 240.0,
      "z_index": 1,
      "visible": true,
      "opacity": 1.0
    }
  ]
}
```

---

## 🧪 Suíte de Testes Automatizados (Pytest)

O OmniMotion conta com cobertura rigorosa de testes unitários e de integração abrangendo todas as camadas (Domain, Application, Infrastructure e Presentation):

```bash
# Executar todos os testes
python3 -m pytest
```

```text
============================= test session starts ==============================
collected 38 items

tests/Application/test_compile_artifact.py ....                          [ 10%]
tests/Application/test_extract_layout_specification.py ...               [ 18%]
tests/Domain/test_dimensions.py .....                                    [ 31%]
tests/Domain/test_media_layer.py .....                                   [ 44%]
tests/Domain/test_motion_timeline.py ......                              [ 60%]
tests/Infrastructure/test_agents.py ..                                   [ 65%]
tests/Infrastructure/test_compiler_factory.py ...                        [ 73%]
tests/Infrastructure/test_crewai_video_analyzer.py ......                [ 89%]
tests/Presentation/test_cli.py ....                                      [100%]

============================== 38 passed in 0.10s ==============================
```

---

## 🛠️ Compiladores de Artefatos Suportados

A partir do `MotionTimeline` gerado, a camada de infraestrutura utiliza compiladores especializados para gerar saídas executáveis:
- **AstroCompiler**: Compila a especificação em um componente Astro com animações CSS/Tailwind prontas para a web.
- **MP4Compiler**: Renderiza um vídeo reconstruído em MP4 aplicando as transformações de movimento e camadas.
