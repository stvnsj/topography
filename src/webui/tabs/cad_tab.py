from __future__ import annotations

import streamlit as st

from webui.services.cad_service import (
    generate_adjusted_coordinates_csv,
    generate_anchos_csv,
    generate_complete_cad,
    generate_fragmented_cad_zip,
    generate_mop_csv,
    generate_tramo_cad,
)


def path_input(label: str, key: str, placeholder: str = "/ruta/al/archivo.csv") -> str:
    return st.text_input(label, key=key, placeholder=placeholder)


def store_result(state_key: str, artifact) -> None:
    st.session_state[state_key] = {
        "name": artifact.name,
        "data": artifact.data,
        "mime": artifact.mime,
        "log": artifact.log,
    }


def show_result(state_key: str) -> None:
    result = st.session_state.get(state_key)
    if not result:
        return

    st.download_button(
        "Descargar",
        data=result["data"],
        file_name=result["name"],
        mime=result["mime"],
        key=f"download::{state_key}",
        use_container_width=True,
    )

    if result["log"]:
        with st.expander("Ver log"):
            st.code(result["log"])


def render_cad_tab() -> None:
    st.subheader("CAD")

    with st.container(border=True):
        st.markdown("#### Archivos base")
        descriptor = path_input("Estacado con Descriptor", "cad_descriptor")
        coordinate = path_input("Estacado con Coordenadas", "cad_coordinate")
        longitudinal = path_input("Longitudinal", "cad_longitudinal")

    with st.container(border=True):
        st.markdown("#### Parámetros comunes")
        col1, col2, col3 = st.columns(3)

        with col1:
            stack_length = st.number_input(
                "Perfiles por fila",
                min_value=1,
                value=1,
                step=1,
            )

        with col2:
            yscale = st.number_input(
                "Escala vertical",
                min_value=0.0,
                value=1.0,
                step=0.1,
            )

        with col3:
            cerco = st.checkbox("Cercos", value=False)

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

            c1, c2 = st.columns(2)
            with c1:
                meter0 = st.number_input("Metros Inicio", min_value=0.0, value=0.0, step=1.0)
            with c2:
                meter1 = st.number_input("Metros Final", min_value=0.0, value=100.0, step=1.0)

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

            project_name = st.text_input("Nombre Proyecto")
            chunk_size = st.number_input("Perfiles por archivo", min_value=1, value=50, step=1)

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

            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("MOP", use_container_width=True):
                    try:
                        artifact = generate_mop_csv(descriptor, coordinate, longitudinal)
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_mop", artifact)

                show_result("cad_mop")

            with c2:
                if st.button("Coordenadas ajustadas", use_container_width=True):
                    try:
                        artifact = generate_adjusted_coordinates_csv(descriptor, coordinate, longitudinal)
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_coordz", artifact)

                show_result("cad_coordz")

            with c3:
                if st.button("Anchos", use_container_width=True):
                    try:
                        artifact = generate_anchos_csv(descriptor, coordinate, longitudinal)
                    except Exception as e:
                        st.error(str(e))
                    else:
                        store_result("cad_anchos", artifact)

                show_result("cad_anchos")