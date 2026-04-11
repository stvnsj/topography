from __future__ import annotations

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from webui.services.cad_service import (
    GeneratedArtifact,
    generate_adjusted_coordinates_csv,
    generate_anchos_csv,
    generate_complete_cad,
    generate_fragmented_cad_zip,
    generate_mop_csv,
    generate_tramo_cad,
)

st.set_page_config(
    page_title="Sistema de Procesamiento Topográfico",
    page_icon="📐",
    layout="wide",
)


def store_result(key: str, artifact: GeneratedArtifact) -> None:
    st.session_state[key] = artifact


def show_result(key: str) -> None:
    artifact = st.session_state.get(key)
    if artifact is None:
        return

    st.download_button(
        label=f"Descargar {artifact.name}",
        data=artifact.data,
        file_name=artifact.name,
        mime=artifact.mime,
        key=f"download::{key}",
        use_container_width=True,
    )

    if artifact.log:
        with st.expander("Ver log"):
            st.code(artifact.log)


def render_cad_tab() -> None:
    st.subheader("CAD")

    with st.container(border=True):
        st.markdown("#### Archivos base")
        descriptor = st.text_input(
            "Estacado con Descriptor",
            placeholder="/ruta/al/descriptor.csv",
            key="cad_descriptor",
        )
        coordinate = st.text_input(
            "Estacado con Coordenadas",
            placeholder="/ruta/al/coordenadas.csv",
            key="cad_coordinate",
        )
        longitudinal = st.text_input(
            "Longitudinal",
            placeholder="/ruta/al/longitudinal.csv",
            key="cad_longitudinal",
        )

    with st.container(border=True):
        st.markdown("#### Parámetros comunes")
        c1, c2, c3 = st.columns(3)

        with c1:
            stack_length = st.number_input(
                "Perfiles por fila",
                min_value=1,
                value=1,
                step=1,
                key="cad_stack_length",
            )

        with c2:
            yscale = st.number_input(
                "Escala vertical",
                min_value=0.0,
                value=1.0,
                step=0.1,
                key="cad_yscale",
            )

        with c3:
            cerco = st.checkbox(
                "Cercos",
                value=False,
                key="cad_cerco",
            )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("#### CAD Proyecto Completo")

            if st.button("Generar CAD completo", use_container_width=True):
                try:
                    artifact = generate_complete_cad(
                        descriptor=descriptor,
                        coordinate=coordinate,
                        longitudinal=longitudinal,
                        stack_length=stack_length,
                        yscale=yscale,
                        cerco=cerco,
                    )
                except Exception as e:
                    st.error(str(e))
                else:
                    store_result("cad_complete", artifact)
                    st.success("Archivo generado")

            show_result("cad_complete")

        with st.container(border=True):
            st.markdown("#### CAD de Tramo")

            t1, t2 = st.columns(2)
            with t1:
                meter0 = st.number_input(
                    "Metros Inicio",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key="cad_meter0",
                )
            with t2:
                meter1 = st.number_input(
                    "Metros Final",
                    min_value=0.0,
                    value=100.0,
                    step=1.0,
                    key="cad_meter1",
                )

            if st.button("Generar CAD tramo", use_container_width=True):
                try:
                    artifact = generate_tramo_cad(
                        descriptor=descriptor,
                        coordinate=coordinate,
                        longitudinal=longitudinal,
                        meter0=meter0,
                        meter1=meter1,
                        stack_length=stack_length,
                        yscale=yscale,
                        cerco=cerco,
                    )
                except Exception as e:
                    st.error(str(e))
                else:
                    store_result("cad_tramo", artifact)
                    st.success("Archivo generado")

            show_result("cad_tramo")

    with right:
        with st.container(border=True):
            st.markdown("#### CAD Proyecto Fragmentado")

            project_name = st.text_input(
                "Nombre Proyecto",
                key="cad_project_name",
            )

            chunk_size = st.number_input(
                "Perfiles por archivo",
                min_value=1,
                value=50,
                step=1,
                key="cad_chunk_size",
            )

            if st.button("Generar ZIP fragmentado", use_container_width=True):
                try:
                    artifact = generate_fragmented_cad_zip(
                        descriptor=descriptor,
                        coordinate=coordinate,
                        longitudinal=longitudinal,
                        stack_length=stack_length,
                        chunk_size=chunk_size,
                        project_name=project_name,
                        yscale=yscale,
                        cerco=cerco,
                    )
                except Exception as e:
                    st.error(str(e))
                else:
                    store_result("cad_fragmented", artifact)
                    st.success("ZIP generado")

            show_result("cad_fragmented")

        with st.container(border=True):
            st.markdown("#### Planillas")

            p1, p2, p3 = st.columns(3)

            with p1:
                if st.button("MOP", use_container_width=True):
                    try:
                        artifact = generate_mop_csv(
                            descriptor=descriptor,
                            coordinate=coordinate,
                            longitudinal=longitudinal,
                        )
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_mop", artifact)

                show_result("cad_mop")

            with p2:
                if st.button("Coordenadas ajustadas", use_container_width=True):
                    try:
                        artifact = generate_adjusted_coordinates_csv(
                            descriptor=descriptor,
                            coordinate=coordinate,
                            longitudinal=longitudinal,
                        )
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_coordz", artifact)

                show_result("cad_coordz")

            with p3:
                if st.button("Anchos", use_container_width=True):
                    try:
                        artifact = generate_anchos_csv(
                            descriptor=descriptor,
                            coordinate=coordinate,
                            longitudinal=longitudinal,
                        )
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_anchos", artifact)

                show_result("cad_anchos")


def render_placeholder_tab(title: str) -> None:
    st.subheader(title)
    st.info("Pendiente de migración")


def main() -> None:
    st.title("Sistema de Procesamiento Topográfico")

    tabs = st.tabs([
        "CAD",
        "NIVELACION",
        "ANEXO (Ante.)",
        "ANEXO (Def.)",
        "PLOT",
        "CONTROL",
        "HERRAMIENTAS",
    ])

    with tabs[0]:
        render_cad_tab()

    with tabs[1]:
        render_placeholder_tab("NIVELACION")

    with tabs[2]:
        render_placeholder_tab("ANEXO (Ante.)")

    with tabs[3]:
        render_placeholder_tab("ANEXO (Def.)")

    with tabs[4]:
        render_placeholder_tab("PLOT")

    with tabs[5]:
        render_placeholder_tab("CONTROL")

    with tabs[6]:
        render_placeholder_tab("HERRAMIENTAS")


if __name__ == "__main__":
    main()