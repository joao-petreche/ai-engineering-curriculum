"""
Script de inspeção de arquivos IDF usando Eppy.
Mês 1 - Exercício 2.1

Este script analisa a estrutura de um arquivo IDF do EnergyPlus
e extrai informações sobre building, zonas, materiais e superfícies.
"""

from pathlib import Path
from eppy.modeleditor import IDF
import json
import sys

# Configurações
ENERGYPLUS_DIR = Path("C:/EnergyPlusV24-1-0")
IDD_FILE = ENERGYPLUS_DIR / "Energy+.idd"

def initialize_idd():
    """Inicializa arquivo IDD do EnergyPlus"""
    if not IDD_FILE.exists():
        print(f"❌ Arquivo IDD não encontrado: {IDD_FILE}")
        print(f"   Verifique se EnergyPlus está instalado em: {ENERGYPLUS_DIR}")
        sys.exit(1)
    
    IDF.setiddname(str(IDD_FILE))

def inspect_idf(idf_path):
    """
    Inspeciona arquivo IDF e extrai informações estruturais.
    
    Args:
        idf_path: Caminho para arquivo .idf
    
    Returns:
        dict: Estrutura do IDF
    """
    
    print(f"🔍 Inspecionando: {idf_path}\n")
    
    idf_path = Path(idf_path)
    if not idf_path.exists():
        print(f"❌ Arquivo IDF não encontrado: {idf_path}")
        sys.exit(1)
    
    # Carregar IDF
    try:
        idf = IDF(str(idf_path))
    except Exception as e:
        print(f"❌ Erro ao carregar IDF: {e}")
        sys.exit(1)
    
    # 1. Listar todos os tipos de objetos
    print("📋 Tipos de Objetos no IDF:")
    print("-" * 70)
    
    object_types = idf.idfobjects.keys()
    object_summary = {}
    
    for obj_type in sorted(object_types):
        count = len(idf.idfobjects[obj_type])
        if count > 0:
            object_summary[obj_type] = count
            print(f"  {obj_type:.<60} {count:>3} objeto(s)")
    
    print(f"\n{'Total de tipos de objetos:':.<60} {len(object_summary):>3}")
    
    # 2. Inspecionar Building
    print("\n🏢 Informações do Building:")
    print("-" * 70)
    buildings = idf.idfobjects['BUILDING']
    building_info = None
    
    if buildings:
        building = buildings[0]
        building_info = {
            "name": building.Name,
            "north_axis": float(building.North_Axis) if building.North_Axis else 0.0,
            "terrain": building.Terrain if hasattr(building, 'Terrain') else "Unknown"
        }
        print(f"  Nome: {building_info['name']}")
        print(f"  Norte: {building_info['north_axis']}°")
        print(f"  Terreno: {building_info['terrain']}")
    else:
        print("  ⚠️  Nenhum objeto BUILDING encontrado")
    
    # 3. Inspecionar Zones
    print("\n🏠 Zonas Térmicas:")
    print("-" * 70)
    zones = idf.idfobjects['ZONE']
    zone_info = []
    
    if zones:
        for zone in zones:
            info = {
                "name": zone.Name,
                "multiplier": int(zone.Multiplier) if zone.Multiplier else 1,
                "coordinates": {
                    "x": float(zone.X_Origin) if zone.X_Origin else 0.0,
                    "y": float(zone.Y_Origin) if zone.Y_Origin else 0.0,
                    "z": float(zone.Z_Origin) if zone.Z_Origin else 0.0
                }
            }
            zone_info.append(info)
            
            print(f"  • {info['name']}")
            print(f"    Multiplicador: {info['multiplier']}")
            print(f"    Coordenadas: X={info['coordinates']['x']}, "
                  f"Y={info['coordinates']['y']}, Z={info['coordinates']['z']}")
    else:
        print("  ⚠️  Nenhuma zona térmica encontrada")
    
    # 4. Inspecionar Materiais
    print("\n🧱 Materiais:")
    print("-" * 70)
    materials = idf.idfobjects['MATERIAL']
    material_info = []
    
    if materials:
        for mat in materials:
            info = {
                "name": mat.Name,
                "thickness": float(mat.Thickness) if mat.Thickness else 0.0,
                "conductivity": float(mat.Conductivity) if mat.Conductivity else 0.0,
                "density": float(mat.Density) if mat.Density else 0.0,
                "specific_heat": float(mat.Specific_Heat) if mat.Specific_Heat else 0.0
            }
            material_info.append(info)
            
            print(f"  • {info['name']}")
            print(f"    Espessura: {info['thickness']:.4f} m")
            print(f"    Condutividade: {info['conductivity']:.3f} W/m-K")
            print(f"    Densidade: {info['density']:.1f} kg/m³")
            print(f"    Calor Específico: {info['specific_heat']:.0f} J/kg-K")
    else:
        print("  ⚠️  Nenhum material encontrado")
    
    # 5. Inspecionar Superfícies (BuildingSurface:Detailed)
    print("\n🔲 Superfícies:")
    print("-" * 70)
    surfaces = idf.idfobjects['BUILDINGSURFACE:DETAILED']
    
    surface_types = {}
    surface_info = []
    
    if surfaces:
        for surf in surfaces:
            surf_type = surf.Surface_Type
            surface_types[surf_type] = surface_types.get(surf_type, 0) + 1
            
            surface_info.append({
                "name": surf.Name,
                "type": surf_type,
                "construction": surf.Construction_Name if hasattr(surf, 'Construction_Name') else "Unknown",
                "zone": surf.Zone_Name if hasattr(surf, 'Zone_Name') else "Unknown"
            })
        
        for surf_type, count in sorted(surface_types.items()):
            print(f"  {surf_type:.<60} {count:>3}")
    else:
        print("  ⚠️  Nenhuma superfície encontrada")
    
    # 6. Inspecionar Construções
    print("\n🏗️  Construções:")
    print("-" * 70)
    constructions = idf.idfobjects['CONSTRUCTION']
    construction_info = []
    
    if constructions:
        for const in constructions:
            layers = []
            # Extrair layers (Outside_Layer, Layer_2, Layer_3, etc)
            for i in range(2, 10):  # Máximo 8 layers
                layer_attr = f"Layer_{i}" if i > 1 else "Outside_Layer"
                if hasattr(const, layer_attr):
                    layer = getattr(const, layer_attr)
                    if layer:
                        layers.append(layer)
            
            info = {
                "name": const.Name,
                "layers": layers
            }
            construction_info.append(info)
            
            print(f"  • {info['name']}")
            print(f"    Camadas ({len(layers)}): {', '.join(layers)}")
    else:
        print("  ⚠️  Nenhuma construção encontrada")
    
    # 7. Criar estrutura completa
    structure = {
        "file_path": str(idf_path),
        "object_counts": object_summary,
        "building": building_info,
        "zones": zone_info,
        "materials": material_info,
        "constructions": construction_info,
        "surfaces": {
            "by_type": surface_types,
            "details": surface_info
        }
    }
    
    return structure

def export_structure(structure, output_path="output/idf_structure.json"):
    """
    Exporta estrutura IDF para JSON.
    
    Args:
        structure: Dicionário com estrutura IDF
        output_path: Caminho do arquivo de saída
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Estrutura exportada para: {output_path.absolute()}")

def main():
    """Função principal"""
    print("="*70)
    print("INSPEÇÃO DE ARQUIVO IDF - MÊS 1, EXERCÍCIO 2.1")
    print("="*70)
    print()
    
    # Inicializar IDD
    initialize_idd()
    
    # Arquivo IDF padrão
    idf_file = ENERGYPLUS_DIR / "ExampleFiles/1ZoneUncontrolled.idf"
    
    # Permitir arquivo customizado via argumento
    if len(sys.argv) > 1:
        idf_file = Path(sys.argv[1])
    
    # Inspecionar
    structure = inspect_idf(idf_file)
    
    # Exportar
    export_structure(structure)
    
    print("\n" + "="*70)
    print("✅ INSPEÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print(f"\n💡 Próximo passo: Analisar output/idf_structure.json")
    print(f"   Use este comando para visualizar:")
    print(f"   cat output/idf_structure.json | python -m json.tool")

if __name__ == "__main__":
    main()
