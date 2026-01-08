import json
import re

# Leer la colección
with open('NeoCare_Postman_Collection_Updated.json', 'r', encoding='utf-8') as f:
    collection = json.load(f)

def fix_test_script(script_lines):
    """Elimina variables locales redundantes y usa pm.response directamente"""
    fixed_lines = []
    skip_next_empty = False
    
    for line in script_lines:
        # Eliminar declaraciones de responseCode y responseData
        if ('const responseCode' in line or 'let responseCode' in line or
            'const responseData' in line or 'let responseData' in line):
            skip_next_empty = True
            continue
        
        # Eliminar línea vacía después de declaraciones eliminadas
        if skip_next_empty and line.strip() == '':
            skip_next_empty = False
            continue
        
        skip_next_empty = False
        
        # Reemplazar responseCode por pm.response.code
        if 'responseCode' in line:
            line = line.replace('responseCode', 'pm.response.code')
        
        # Reemplazar responseData por pm.response.json()
        if 'responseData' in line:
            # Para accesos a propiedades: responseData.access_token
            if 'responseData.' in line:
                line = line.replace('responseData.', 'pm.response.json().')
            # Para expect(responseData)
            elif 'expect(responseData)' in line:
                line = line.replace('expect(responseData)', 'expect(pm.response.json())')
            # Otros casos
            else:
                line = line.replace('responseData', 'pm.response.json()')
        
        fixed_lines.append(line)
    
    return fixed_lines

def process_item(item):
    """Procesa un item o carpeta de la colección recursivamente"""
    # Si tiene sub-items (es una carpeta), procesar recursivamente
    if 'item' in item:
        for subitem in item['item']:
            process_item(subitem)
    
    # Procesar eventos de este item
    if 'event' in item:
        for event in item['event']:
            if event.get('listen') == 'test' and 'script' in event and 'exec' in event['script']:
                original_lines = len(event['script']['exec'])
                event['script']['exec'] = fix_test_script(event['script']['exec'])
                fixed_lines = len(event['script']['exec'])
                if original_lines != fixed_lines:
                    print(f"  📝 {item.get('name', 'Unknown')}: {original_lines} → {fixed_lines} líneas")

# Procesar todos los items
print("🔧 Corrigiendo scripts de test...")
for item in collection['item']:
    process_item(item)

# Guardar la colección corregida
with open('NeoCare_Postman_Collection_Updated.json', 'w', encoding='utf-8') as f:
    json.dump(collection, f, indent=2, ensure_ascii=False)

print("\n✅ Colección corregida - Variables locales eliminadas")
print("📦 Archivo: NeoCare_Postman_Collection_Updated.json")
print("🚀 Listo para importar en Postman")
