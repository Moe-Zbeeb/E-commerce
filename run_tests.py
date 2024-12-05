import os
import subprocess

def run_tests_with_coverage():
    try:
        # Ensure clean coverage environment
        if os.path.exists('.coverage'):
            os.remove('.coverage')
        if os.path.exists('htmlcov'):
            subprocess.run(['rm', '-rf', 'htmlcov'], check=True)

        print("Running tests for 'reviews' and 'app' modules with coverage reporting...\n")
        
        # Run pytest with coverage for specific modules
        subprocess.run([
            'pytest', '--cov=app.routes.review', '--cov=app',
            '--cov-report=term-missing', '--cov-report=html'
        ], check=True)
        
        # Inform user about HTML report location
        print("\nCoverage report generated. Open 'htmlcov/index.html' in your browser to view details.\n")

    except subprocess.CalledProcessError as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    run_tests_with_coverage()
