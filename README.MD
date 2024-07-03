# DownTube

Um aplicativo de desktop simples para baixar vídeos do YouTube com a opção de separar por capítulos. Este aplicativo suporta Windows, Linux e macOS.

## Funcionalidades

- Baixa vídeos ou áudios do YouTube.
- Opção para separar vídeos por capítulos.
- Escolha do diretório de salvamento.
- Barra de progresso e status do download.
- Integração com FFmpeg sem necessidade de instalação adicional pelo usuário.

## Requisitos

- Python 3.6 ou superior.
- yt-dlp
- tkinter (geralmente já incluído na instalação padrão do Python)

## Instalação

### Passo 1: Clonar o Repositório

```sh
git clone https://github.com/seu-usuario/youtube-downloader.git
cd youtube-downloader

```

## Passo 2: Instalar Dependências

### Instale as dependências necessárias

```sh

pip install yt-dlp
pip install pyinstaller

```

## Passo 3: Baixar o FFmpeg

### Baixe o binário do FFmpeg correspondente ao seu sistema operacional e coloque-o nas respectivas pastas

Windows: ffmpeg/windows/ffmpeg.exe
Linux: ffmpeg/linux/ffmpeg
macOS: ffmpeg/macos/ffmpeg

## Passo 4: Criar o Executável

### Para criar um executável para seu sistema operacional, use o PyInstaller

```sh

pyinstaller youtube_downloader.spec

```

O executável será gerado na pasta '**dist**'.

## Uso

### Executar o Script Python

Se preferir executar o script Python diretamente:

```sh

python youtube_downloader.py

```

### Executar o Executável

Se você gerou o executável, navegue até a pasta dist e execute:

- **Windows**: youtube_downloader.exe
- **Linux**: ./youtube_downloader
- **macOS**: ./youtube_downloader

Estrutura do Projeto

```arduino

your_project/
│
├── ffmpeg/
│   ├── windows/
│   │   └── ffmpeg.exe
│   ├── linux/
│   │   └── ffmpeg
│   └── macos/
│       └── ffmpeg
│
├── youtube_downloader.py
├── setup.py
├── youtube_downloader.spec
└── ...
```

## Como Funciona

1. **URL do vídeo:** Insira a URL do vídeo do YouTube que deseja baixar.
2. **Formato:** Selecione o formato desejado (mp4 ou mp3).
3. **Separar por capítulos:** Marque a caixa se desejar separar o vídeo por capítulos.
4. **Selecionar Diretório:** Escolha o diretório onde deseja salvar o vídeo/áudio.
5. **Baixar:** Clique no botão "Baixar" para iniciar o download.

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (**'git checkout -b feature/nova-feature'**).
3. Commit suas mudanças (**'git commit -am 'Adiciona nova feature''**).
4. Push para a branch (**'git push origin feature/nova-feature'**).
5. Crie um novo Pull Request.

### Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](https://github.com/di-ferreira/downtube/blob/master/LICENSE) para mais detalhes.

### Créditos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
