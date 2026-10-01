FROM node:20-bookworm-slim@sha256:2cf067cfed83d5ea958367df9f966191a942351a2df77d6f0193e162b5febfc0
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv fonts-noto-cjk git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install -g pnpm@8.4.0
RUN python3 -m venv /opt/travel-tools && /opt/travel-tools/bin/pip install --no-cache-dir Pillow==11.3.0 google-auth-oauthlib==1.2.2 google-api-python-client==2.182.0
ENV PATH="/opt/travel-tools/bin:${PATH}"
WORKDIR /app
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
