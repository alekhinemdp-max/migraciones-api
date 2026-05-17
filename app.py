from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar():
    datos = request.json
    expediente = datos.get('expediente')
    fecha_nac = datos.get('fecha_nac')
    
    session = requests.Session()
    
    # Obtener cookies de sesión
    session.get('https://www.migraciones.gob.ar/accesible/consultaTramitePrecaria/ConsultaUnificada.php', timeout=10)
    
    # Consultar trámite
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.migraciones.gob.ar/accesible/consultaTramitePrecaria/ConsultaUnificada.php',
        'Origin': 'https://www.migraciones.gob.ar'
    }
    
    payload = {'data': f'{{"nro_expediente":"{expediente}","fecha_nac":"{fecha_nac}"}}'}
    
    resp = session.post(
    'https://www.migraciones.gob.ar/accesible/consultaTramitePrecaria/ajax_consulta_tramite.php',
    data=payload,
    headers=headers,
    timeout=10
)
    
    try:
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e), 'raw': resp.text[:500]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
