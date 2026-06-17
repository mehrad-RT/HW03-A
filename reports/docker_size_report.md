# HW03 Docker Image Size Report

| Repository             | Tag       | Size   |
|------------------------|-----------|--------|
| qbc12-airbnb-serving   | naive     | 4.35GB |
| qbc12-airbnb-serving   | optimized | 1.29GB |

## Analysis
The naive image uses the full python:3.11 base image and copies the entire project into the image, so it includes more operating-system packages and non-runtime files.

The optimized image uses python:3.11-slim, installs dependencies in a builder stage, and copies only runtime dependencies plus the service source into the final image. I would use the optimized image in production because it is smaller, faster to pull, and has less unnecessary surface area.
