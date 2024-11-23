import coverage
import pytest
import os

def run_tests_with_coverage():
    # Crear directorio coverage si no existe
    if not os.path.exists('coverage'):
        os.makedirs('coverage')

    # Configurar coverage
    cov = coverage.Coverage(
        source=['app'],
        omit=[
            '*/migrations/*',
            '*/tests/*',
            '*/__init__.py'
        ],
        branch=True
    )

    # Iniciar coverage
    cov.start()

    # Ejecutar tests
    test_files = [
        'app/testApi.py',
        'app/testDbConnection.py',
        'app/testEndpoints.py',
        'app/testHealth.py',
        'app/testInitDb.py',
        'app/testMonitoring.py',
        'app/testRecommendation.py'
    ]
    
    pytest.main(['-v'] + test_files)

    # Detener coverage
    cov.stop()
    
    # Guardar reporte
    cov.save()
    
    # Generar reporte HTML
    cov.html_report(directory='coverage/html')
    
    # Mostrar reporte en consola
    percentage = cov.report()
    
    # Guardar porcentaje en archivo
    with open('coverage/coverage.txt', 'w') as f:
        f.write(str(percentage))

    print(f"Code coverage: {percentage}%")
    return percentage

if __name__ == '__main__':
    run_tests_with_coverage()