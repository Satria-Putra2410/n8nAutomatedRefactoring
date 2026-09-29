import requests
import json
import os

# ==============================
# Konfigurasi
# ==============================

SONARQUBE_URL = "http://localhost:9000"

# SONARQUBE_TOKEN = "YourToken"

# ORGANIZATION = "YourOrganization"
# PROJECT_KEY = "YourProjectKey"
OUTPUT_FILE = "detailed_sonarqube_maintainability_issue.json"

ALLOWED_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx")


def fetch_all_issues():

    if not SONARQUBE_TOKEN:
        raise RuntimeError(
            "SONARQUBE_TOKEN belum diset sebagai environment variable."
        )

    api_url = f"{SONARQUBE_URL}/api/issues/search"

    auth = (SONARQUBE_TOKEN, "")

    all_issues = []

    page = 1
    page_size = 500

    print(f"--- Memulai pengambilan issue ---")
    print(f"Project      : {PROJECT_KEY}")
    print(f"Organization : {ORGANIZATION}")
    print(f"Endpoint     : {api_url}")

    try:

        while True:

            params = {
                "componentKeys": PROJECT_KEY,
                "organization": ORGANIZATION,
                "p": page,
                "ps": page_size
            }

            print(f"\nMengambil halaman {page}...")

            response = requests.get(
                api_url,
                params=params,
                auth=auth,
                timeout=60
            )

            print(f"HTTP Status: {response.status_code}")

            if response.status_code != 200:

                print("Response dari SonarCloud:")
                print(response.text)

                response.raise_for_status()

            data = response.json()

            issues_on_page = data.get("issues", [])

            print(
                f"Issue diterima pada halaman {page}: "
                f"{len(issues_on_page)}"
            )

            # ==============================
            # Proses issue
            # ==============================

            for issue in issues_on_page:

                component = issue.get("component", "")

                if component.endswith(ALLOWED_EXTENSIONS):

                    relevant_issue = {
                        "file_path": component.split(":", 1)[-1],
                        "rule": issue.get("rule"),
                        "severity": issue.get("severity"),
                        "type": issue.get("type"),
                        "message": issue.get("message"),
                        "line": issue.get("line"),
                        "textRange": issue.get("textRange")
                    }

                    all_issues.append(relevant_issue)

            print(
                f"Total issue relevan sejauh ini: "
                f"{len(all_issues)}"
            )

            # ==============================
            # Pagination
            # ==============================

            paging = data.get("paging", {})

            total = paging.get("total")

            if total is not None:

                print(
                    f"Total issue menurut SonarCloud: "
                    f"{total}"
                )

                if page * page_size >= total:
                    break

            else:

                # Jika jumlah issue yang diterima
                # kurang dari page_size, berarti
                # kemungkinan sudah halaman terakhir.

                if len(issues_on_page) < page_size:
                    break

            page += 1

        # ==============================
        # Simpan hasil
        # ==============================

        final_output = {
            "issues": all_issues
        }

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                final_output,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("\n--- Selesai ---")

        print(
            f"Total {len(all_issues)} issue relevan "
            f"telah disimpan ke: {OUTPUT_FILE}"
        )

    except requests.exceptions.RequestException as e:

        print(f"\nError HTTP/koneksi: {e}")

    except Exception as e:

        print(f"\nError yang tidak terduga: {e}")


if __name__ == "__main__":
    fetch_all_issues()