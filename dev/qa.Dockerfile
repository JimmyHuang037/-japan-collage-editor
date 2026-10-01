FROM japan-collage-dev:local
RUN /opt/travel-tools/bin/pip install --no-cache-dir playwright==1.61.0 \
    && /opt/travel-tools/bin/python -m playwright install-deps chromium
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
