from pathlib import Path
from xml.etree import ElementTree

import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.util import interval_lifecycle
from pm4py.objects.log.exporter.xes import exporter as xes_exporter


def convert_xes_to_csv(xes_path: Path, output_path: Path):
    log = pm4py.read_xes(str(xes_path))
    log_interval = interval_lifecycle.to_interval(log)
    df = log_converter.apply(log_interval, variant=log_converter.Variants.TO_DATA_FRAME)
    df.to_csv(output_path, index=False)


def convert_csv_to_xes(csv_path: Path, output_path: Path):
    df = pd.read_csv(csv_path)

    # drop all columns that start with @@
    columns_to_drop = [name for name in df.columns if name.startswith('@@')]
    df.drop(columns_to_drop, axis=1, inplace=True)

    log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)
    log_lifecycle = interval_lifecycle.to_lifecycle(log)
    xes_exporter.apply(log_lifecycle, str(output_path))

    # fixing the timestamp XML tag after pm4py conversion
    ElementTree.register_namespace('', 'http://www.xes-standard.org/')
    root = ElementTree.parse(str(output_path))
    for elem in root.findall(".//*[@key='time:timestamp']"):
        elem.tag = 'date'
    root.write(str(output_path), encoding='utf-8', xml_declaration=True)
