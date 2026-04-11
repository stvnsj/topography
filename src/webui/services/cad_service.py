from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile

import refactorModel.model as model
import refactorCad.cad as cad
import spreadsheet.coordinates as coor
import spreadsheet.mop as mop
import spreadsheet.width as width


@dataclass
class GeneratedArtifact:
    name: str
    data: bytes
    mime: str
    log: str = ""


def _capture_logs(fn) -> str:
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        fn()

    out = stdout.getvalue().strip()
    err = stderr.getvalue().strip()

    if out and err:
        return f"{out}\n\n{err}"
    return out or err or ""


def _require_nonempty(value: str, label: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"Falta el archivo: {label}")
    return value


def _positive_int(value: int | float, label: str) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{label} debe ser un entero > 0")
    return value


def _nonnegative_float(value: int | float, label: str) -> float:
    value = float(value)
    if value < 0:
        raise ValueError(f"{label} debe ser un número >= 0")
    return value


def _build_model(descriptor: str, coordinate: str, longitudinal: str):
    descriptor = _require_nonempty(descriptor, "Estacado con Descriptor")
    coordinate = _require_nonempty(coordinate, "Estacado con Coordenadas")
    longitudinal = _require_nonempty(longitudinal, "Longitudinal")

    return model.Model.from_files(
        filename1=descriptor,
        filename2=coordinate,
        filename3=longitudinal,
    )


def _read_bytes(path: Path) -> bytes:
    if not path.exists():
        raise RuntimeError(f"No se generó el archivo esperado: {path}")
    return path.read_bytes()


def _zip_directory(directory: Path) -> bytes:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(directory))

    buffer.seek(0)
    return buffer.read()


def generate_complete_cad(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
    stack_length: int,
    yscale: float,
    cerco: bool,
) -> GeneratedArtifact:
    stack_length = _positive_int(stack_length, "Perfiles por fila")
    yscale = _nonnegative_float(yscale, "Escala vertical")

    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output = Path(td) / "cad_proyecto_completo.scr"

        def run():
            cad.CadScript(
                model1,
                yscale=yscale,
                cerco=cerco,
            ).writeCompleteProject(
                str(output),
                stackSize=stack_length,
            )

        log = _capture_logs(run)
        data = _read_bytes(output)

    return GeneratedArtifact(
        name=output.name,
        data=data,
        mime="text/plain",
        log=log,
    )


def generate_tramo_cad(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
    meter0: float,
    meter1: float,
    stack_length: int,
    yscale: float,
    cerco: bool,
) -> GeneratedArtifact:
    stack_length = _positive_int(stack_length, "Perfiles por fila")
    meter0 = _nonnegative_float(meter0, "Metros Inicio")
    meter1 = _nonnegative_float(meter1, "Metros Final")
    yscale = _nonnegative_float(yscale, "Escala vertical")

    if meter1 <= meter0:
        raise ValueError("Metros Final debe ser mayor que Metros Inicio")

    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output = Path(td) / "cad_tramo.scr"

        def run():
            cad.CadScript(
                model1,
                yscale=yscale,
                cerco=cerco,
            ).writeKm(
                dm0=meter0,
                dm1=meter1,
                stackSize=stack_length,
                fn=str(output),
            )

        log = _capture_logs(run)
        data = _read_bytes(output)

    return GeneratedArtifact(
        name=output.name,
        data=data,
        mime="text/plain",
        log=log,
    )


def generate_fragmented_cad_zip(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
    stack_length: int,
    chunk_size: int,
    project_name: str,
    yscale: float,
    cerco: bool,
) -> GeneratedArtifact:
    stack_length = _positive_int(stack_length, "Perfiles por fila")
    chunk_size = _positive_int(chunk_size, "Perfiles por archivo")
    yscale = _nonnegative_float(yscale, "Escala vertical")
    project_name = (project_name or "").strip()

    if not project_name:
        raise ValueError("Debe ingresar un nombre de proyecto")

    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output_dir = Path(td) / project_name
        output_dir.mkdir(parents=True, exist_ok=True)

        def run():
            cad.CadScript(
                model1,
                yscale=yscale,
                cerco=cerco,
            ).writeFull(
                str(output_dir),
                project_name,
                fileSize=chunk_size,
                stackSize=stack_length,
            )

        log = _capture_logs(run)
        data = _zip_directory(output_dir)

    return GeneratedArtifact(
        name=f"{project_name}.zip",
        data=data,
        mime="application/zip",
        log=log,
    )


def generate_mop_csv(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
) -> GeneratedArtifact:
    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output = Path(td) / "mop.csv"

        def run():
            mop.MopFormat(model1).write(str(output))

        log = _capture_logs(run)
        data = _read_bytes(output)

    return GeneratedArtifact(
        name=output.name,
        data=data,
        mime="text/csv",
        log=log,
    )


def generate_adjusted_coordinates_csv(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
) -> GeneratedArtifact:
    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output = Path(td) / "coordenadas_ajustadas.csv"

        def run():
            coor.AdjustedCoordinateModel(model1).writeCsv(str(output))

        log = _capture_logs(run)
        data = _read_bytes(output)

    return GeneratedArtifact(
        name=output.name,
        data=data,
        mime="text/csv",
        log=log,
    )


def generate_anchos_csv(
    *,
    descriptor: str,
    coordinate: str,
    longitudinal: str,
) -> GeneratedArtifact:
    model1 = _build_model(descriptor, coordinate, longitudinal)

    with TemporaryDirectory() as td:
        output = Path(td) / "anchos.csv"

        def run():
            width.ModelWidth(model1).write(str(output))

        log = _capture_logs(run)
        data = _read_bytes(output)

    return GeneratedArtifact(
        name=output.name,
        data=data,
        mime="text/csv",
        log=log,
    )