#!/usr/bin/env python3
"""Bootstrap a bounded greenfield project with a stronger quality baseline."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


PYTHON_FLASK_FILES = {
    ".gitignore": dedent(
        """\
        .venv/
        __pycache__/
        *.pyc
        .pytest_cache/
        .ruff_cache/
        instance/
        """
    ),
    "pyproject.toml": dedent(
        """\
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "greenfield-flask-app"
        version = "0.1.0"
        description = "Greenfield Flask delivery scaffold"
        requires-python = ">=3.11"
        dependencies = [
          "Flask==3.1.0",
        ]

        [tool.ruff]
        line-length = 100
        target-version = "py311"

        [tool.ruff.lint]
        select = ["E", "F", "I", "B", "UP"]

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        """
    ),
    "README.md": dedent(
        """\
        # Greenfield Flask App

        Bounded Python web scaffold with app factory, tests, and lint baseline.

        ## Run

        ```bash
        python3 -m venv .venv
        . .venv/bin/activate
        pip install -e .
        python run.py
        ```

        ## Quality

        ```bash
        pytest
        ruff check .
        ```
        """
    ),
    "run.py": dedent(
        """\
        from app import create_app


        app = create_app()


        if __name__ == "__main__":
            app.run(debug=True)
        """
    ),
    "app/__init__.py": dedent(
        """\
        from flask import Flask

        from .routes import register_routes


        def create_app() -> Flask:
            app = Flask(__name__)
            app.config["SECRET_KEY"] = "dev-secret"
            register_routes(app)
            return app
        """
    ),
    "app/routes.py": dedent(
        """\
        from flask import Flask, render_template


        def register_routes(app: Flask) -> None:
            @app.get("/")
            def home() -> str:
                return render_template("home.html")
        """
    ),
    "app/templates/home.html": dedent(
        """\
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Greenfield Flask App</title>
            <link rel="stylesheet" href="/static/style.css" />
          </head>
          <body>
            <main class="shell">
              <p class="eyebrow">Greenfield Flask Delivery</p>
              <h1>Start from release-1 scope, not random boilerplate.</h1>
              <p>This scaffold is intentionally small and ready for bounded product work.</p>
            </main>
          </body>
        </html>
        """
    ),
    "app/static/style.css": dedent(
        """\
        body {
          margin: 0;
          font-family: "Segoe UI", sans-serif;
          color: #1f1814;
          background: linear-gradient(180deg, #f9f2e9 0%, #efe2d4 100%);
        }

        .shell {
          width: min(920px, calc(100% - 48px));
          margin: 0 auto;
          padding: 96px 0;
        }

        .eyebrow {
          text-transform: uppercase;
          letter-spacing: 0.18em;
          color: #914725;
          font-size: 0.8rem;
        }

        h1 {
          font-size: clamp(2.6rem, 6vw, 4.4rem);
          line-height: 0.94;
        }
        """
    ),
    "tests/test_smoke.py": dedent(
        """\
        import unittest

        from app import create_app


        class SmokeTestCase(unittest.TestCase):
            def setUp(self) -> None:
                app = create_app()
                app.config.update(TESTING=True)
                self.client = app.test_client()

            def test_home(self) -> None:
                response = self.client.get("/")
                self.assertEqual(response.status_code, 200)


        if __name__ == "__main__":
            unittest.main()
        """
    ),
}


TS_REACT_FILES = {
    ".gitignore": dedent(
        """\
        node_modules/
        dist/
        coverage/
        .DS_Store
        """
    ),
    "package.json": dedent(
        """\
        {
          "name": "greenfield-react-web",
          "private": true,
          "version": "0.1.0",
          "type": "module",
          "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview",
            "lint": "eslint .",
            "test": "vitest run"
          },
          "dependencies": {
            "react": "^18.3.1",
            "react-dom": "^18.3.1"
          },
          "devDependencies": {
            "@testing-library/jest-dom": "^6.6.3",
            "@testing-library/react": "^16.0.1",
            "@testing-library/user-event": "^14.5.2",
            "@types/react": "^18.3.12",
            "@types/react-dom": "^18.3.1",
            "@vitejs/plugin-react": "^4.3.2",
            "eslint": "^9.15.0",
            "eslint-plugin-react-hooks": "^5.0.0",
            "eslint-plugin-react-refresh": "^0.4.14",
            "jsdom": "^25.0.1",
            "typescript": "^5.6.3",
            "typescript-eslint": "^8.15.0",
            "vite": "^5.4.10",
            "vitest": "^2.1.5"
          }
        }
        """
    ),
    "tsconfig.json": dedent(
        """\
        {
          "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": true,
            "lib": ["DOM", "DOM.Iterable", "ES2020"],
            "allowJs": false,
            "skipLibCheck": true,
            "esModuleInterop": true,
            "allowSyntheticDefaultImports": true,
            "strict": true,
            "forceConsistentCasingInFileNames": true,
            "module": "ESNext",
            "moduleResolution": "Node",
            "resolveJsonModule": true,
            "isolatedModules": true,
            "noEmit": true,
            "jsx": "react-jsx"
          },
          "include": ["src", "vitest.setup.ts"]
        }
        """
    ),
    "eslint.config.js": dedent(
        """\
        import js from "@eslint/js";
        import reactHooks from "eslint-plugin-react-hooks";
        import reactRefresh from "eslint-plugin-react-refresh";
        import tseslint from "typescript-eslint";

        export default tseslint.config(
          { ignores: ["dist"] },
          js.configs.recommended,
          ...tseslint.configs.recommended,
          {
            files: ["**/*.{ts,tsx}"],
            plugins: {
              "react-hooks": reactHooks,
              "react-refresh": reactRefresh,
            },
            rules: {
              ...reactHooks.configs.recommended.rules,
              "react-refresh/only-export-components": ["warn", { allowConstantExport: true }],
            },
          },
        );
        """
    ),
    "vite.config.ts": dedent(
        """\
        import { defineConfig } from "vite";
        import react from "@vitejs/plugin-react";

        export default defineConfig({
          plugins: [react()],
          test: {
            environment: "jsdom",
            setupFiles: "./vitest.setup.ts",
          },
        });
        """
    ),
    "vitest.setup.ts": 'import "@testing-library/jest-dom";\n',
    "index.html": dedent(
        """\
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Greenfield React Web</title>
            <script type="module" src="/src/main.tsx"></script>
          </head>
          <body>
            <div id="root"></div>
          </body>
        </html>
        """
    ),
    "src/main.tsx": dedent(
        """\
        import React from "react";
        import ReactDOM from "react-dom/client";
        import { App } from "./App";
        import "./styles.css";

        ReactDOM.createRoot(document.getElementById("root")!).render(
          <React.StrictMode>
            <App />
          </React.StrictMode>,
        );
        """
    ),
    "src/lib/tokens.ts": dedent(
        """\
        export const tokens = {
          ink: "#1d1814",
          accent: "#8f4827",
          canvas: "#f8f0e7",
          panel: "#fffaf4",
        } as const;
        """
    ),
    "src/components/Hero.tsx": dedent(
        """\
        export function Hero() {
          return (
            <section className="hero">
              <p className="eyebrow">Greenfield Web Frontend</p>
              <h1>Design the release slice before the component tree expands.</h1>
              <p className="lead">
                This scaffold starts with a single deliberate page so product hierarchy stays visible.
              </p>
            </section>
          );
        }
        """
    ),
    "src/App.tsx": dedent(
        """\
        import { Hero } from "./components/Hero";

        export function App() {
          return (
            <main className="app-shell">
              <Hero />
            </main>
          );
        }
        """
    ),
    "src/styles.css": dedent(
        """\
        :root {
          color-scheme: light;
          font-family: "Segoe UI", sans-serif;
          color: #1d1814;
          background: #f8f0e7;
        }

        body {
          margin: 0;
          min-height: 100vh;
          background: linear-gradient(180deg, #fbf5ee 0%, #efe0d2 100%);
        }

        .app-shell {
          width: min(960px, calc(100% - 48px));
          margin: 0 auto;
          padding: 96px 0;
        }

        .eyebrow {
          text-transform: uppercase;
          letter-spacing: 0.18em;
          color: #8f4827;
          font-size: 0.8rem;
        }

        h1 {
          font-size: clamp(2.8rem, 6vw, 5rem);
          line-height: 0.94;
          max-width: 720px;
        }

        .lead {
          max-width: 640px;
          line-height: 1.7;
          color: #6d6159;
        }
        """
    ),
    "src/__tests__/app.test.tsx": dedent(
        """\
        import { render, screen } from "@testing-library/react";
        import { App } from "../App";

        describe("App", () => {
          it("renders the release-slice headline", () => {
            render(<App />);
            expect(screen.getByText(/Design the release slice/i)).toBeInTheDocument();
          });
        });
        """
    ),
    "README.md": dedent(
        """\
        # Greenfield React Web

        Bounded TypeScript/React scaffold with lint and test baseline.

        ## Run

        ```bash
        npm install
        npm run dev
        ```

        ## Quality

        ```bash
        npm run lint
        npm run test
        npm run build
        ```
        """
    ),
}


JAVA_SPRING_FILES = {
    ".gitignore": dedent(
        """\
        target/
        .idea/
        *.iml
        .DS_Store
        """
    ),
    "pom.xml": dedent(
        """\
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
          <modelVersion>4.0.0</modelVersion>
          <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>3.3.5</version>
            <relativePath/>
          </parent>
          <groupId>com.example</groupId>
          <artifactId>greenfield-java-service</artifactId>
          <version>0.1.0</version>
          <name>greenfield-java-service</name>
          <description>Greenfield Spring Boot delivery scaffold</description>
          <properties>
            <java.version>21</java.version>
          </properties>
          <dependencies>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-validation</artifactId>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-test</artifactId>
              <scope>test</scope>
            </dependency>
          </dependencies>
          <build>
            <plugins>
              <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
              </plugin>
            </plugins>
          </build>
        </project>
        """
    ),
    "src/main/resources/application.yml": dedent(
        """\
        spring:
          application:
            name: greenfield-java-service
        server:
          port: 8080
        """
    ),
    "src/main/java/com/example/greenfield/GreenfieldApplication.java": dedent(
        """\
        package com.example.greenfield;

        import org.springframework.boot.SpringApplication;
        import org.springframework.boot.autoconfigure.SpringBootApplication;

        @SpringBootApplication
        public class GreenfieldApplication {
            public static void main(String[] args) {
                SpringApplication.run(GreenfieldApplication.class, args);
            }
        }
        """
    ),
    "src/main/java/com/example/greenfield/web/HealthResponse.java": dedent(
        """\
        package com.example.greenfield.web;

        public record HealthResponse(String service, String status) {}
        """
    ),
    "src/main/java/com/example/greenfield/web/HomeController.java": dedent(
        """\
        package com.example.greenfield.web;

        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RestController;

        @RestController
        @RequestMapping("/api")
        public class HomeController {
            @GetMapping("/health")
            public HealthResponse health() {
                return new HealthResponse("greenfield-java-service", "ok");
            }
        }
        """
    ),
    "src/test/java/com/example/greenfield/GreenfieldApplicationTests.java": dedent(
        """\
        package com.example.greenfield;

        import static org.assertj.core.api.Assertions.assertThat;

        import com.example.greenfield.web.HealthResponse;
        import org.junit.jupiter.api.Test;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.boot.test.web.client.TestRestTemplate;
        import org.springframework.boot.test.web.server.LocalServerPort;
        import org.springframework.http.ResponseEntity;

        @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
        class GreenfieldApplicationTests {
            @LocalServerPort
            private int port;

            private final TestRestTemplate restTemplate = new TestRestTemplate();

            @Test
            void healthEndpointReturnsOk() {
                ResponseEntity<HealthResponse> response =
                        restTemplate.getForEntity("http://localhost:" + port + "/api/health", HealthResponse.class);
                assertThat(response.getStatusCode().is2xxSuccessful()).isTrue();
            }
        }
        """
    ),
    "README.md": dedent(
        """\
        # Greenfield Java Service

        Bounded Spring Boot scaffold with test baseline.

        ## Run

        ```bash
        mvn spring-boot:run
        ```

        ## Quality

        ```bash
        mvn test
        ```
        """
    ),
}


STACK_MAP = {
    "java-spring-web": JAVA_SPRING_FILES,
    "python-flask-web": PYTHON_FLASK_FILES,
    "typescript-react-web": TS_REACT_FILES,
}


def write_file(root: Path, relative_path: str, content: str, overwrite: bool) -> None:
    file_path = root / relative_path
    if file_path.exists() and not overwrite:
        raise FileExistsError(f"{relative_path} already exists")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a bounded greenfield project scaffold.")
    parser.add_argument("--project-root", required=True, help="Target directory for the new project")
    parser.add_argument(
        "--stack",
        required=True,
        choices=sorted(STACK_MAP),
        help="Scaffold profile to generate",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    root.mkdir(parents=True, exist_ok=True)

    for relative_path, content in STACK_MAP[args.stack].items():
        write_file(root, relative_path, content, overwrite=args.overwrite)

    print(f"Bootstrapped {args.stack} at {root}")
    print("Next step: write the Greenfield Bootstrap Plan, Architecture Contract, and release-1 scope.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
