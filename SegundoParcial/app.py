from flask import Flask, request, jsonify

app = Flask(__name__)

tareas_db = [
    {"id": "t-101", "titulo": "Diseño de base de datos", "curso": "Sistemas", "fechaEntrega": "2026-10-01T23:59:00Z", "estado": "completada"},
    {"id": "t-102", "titulo": "Investigación sobre Patrones de Diseño", "curso": "Ingeniería de Software", "fechaEntrega": "2026-10-02T23:59:00Z", "estado": "pendiente"},
    {"id": "t-103", "titulo": "Prototipo de dashboard", "curso": "Interfaces", "fechaEntrega": "2026-10-05T23:59:00Z", "estado": "pendiente"}
]

@app.route('/api/v1/tareas', methods=['GET'])
def obtener_tareas():
    estado_filtro = request.args.get('estado')
    
    if estado_filtro:
        if estado_filtro not in ['pendiente', 'completada']:
            return jsonify({
                "codigoError": "ESTADO_INVALIDO",
                "mensaje": "El estado debe ser 'pendiente' o 'completada'."
            }), 400
            
        tareas_filtradas = [t for t in tareas_db if t['estado'] == estado_filtro]
        return jsonify(tareas_filtradas), 200

    return jsonify(tareas_db), 200

@app.route('/api/v1/tareas/<id_tarea>', methods=['GET'])
def obtener_tarea_individual(id_tarea):
    tarea = next((t for t in tareas_db if t['id'] == id_tarea), None)
    
    if tarea:
        return jsonify(tarea), 200
        
    return jsonify({
        "codigoError": "TAREA_NO_ENCONTRADA",
        "mensaje": f"La tarea con el ID '{id_tarea}' no existe o fue eliminada.",
        "estadoHttp": 404
    }), 404

@app.route('/api/v1/tareas/<id_tarea>', methods=['PATCH'])
def actualizar_tarea(id_tarea):
    tarea = next((t for t in tareas_db if t['id'] == id_tarea), None)
    
    if not tarea:
        return jsonify({
            "codigoError": "TAREA_NO_ENCONTRADA",
            "mensaje": f"La tarea con el ID '{id_tarea}' no existe.",
            "estadoHttp": 404
        }), 404
        
    datos = request.get_json()
    
    if not datos or 'estado' not in datos:
        return jsonify({
            "codigoError": "FALTA_CAMPO",
            "mensaje": "Se requiere el campo 'estado' en el cuerpo de la petición JSON."
        }), 400
        
    nuevo_estado = datos['estado']
    if nuevo_estado not in ['pendiente', 'completada']:
        return jsonify({
            "codigoError": "ESTADO_INVALIDO",
            "mensaje": "El estado debe ser 'pendiente' o 'completada'."
        }), 400
        
    # Actualizar la tarea
    tarea['estado'] = nuevo_estado
    return jsonify(tarea), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)