"""
Handles formatting output of for Pdfalyzezr() class. Split out this way makes Pdfalyzer more of a pure tree
"""
from collections import defaultdict
from typing import Optional

from anytree import LevelOrderIter, RenderTree, SymlinkNode
from anytree.render import DoubleStyle
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from yaralyzer.config import YaralyzerConfig
from yaralyzer.output.rich_console import BYTES_HIGHLIGHT, console
from yaralyzer.output.rich_layout_elements import bytes_hashes_table
from yaralyzer.util.logging import log

from pdfalyzer.binary.binary_scanner import BinaryScanner
from pdfalyzer.decorators.pdf_tree_node import DECODE_FAILURE_LEN
from pdfalyzer.detection.yaralyzer_helper import get_bytes_yaralyzer, get_file_yaralyzer
from pdfalyzer.helpers.string_helper import pp
from pdfalyzer.output.layout import print_section_header, print_section_subheader, print_section_sub_subheader
from pdfalyzer.output.pdf_node_rich_table import generate_rich_tree, get_symlink_representation
from pdfalyzer.output.stream_objects_table import stream_objects_table
from pdfalyzer.pdfalyzer import Pdfalyzer
from pdfalyzer.util.adobe_strings import *


class PdfalyzerPresenter:
    def __init__(self, pdfalyzer: Pdfalyzer):
        self.pdfalyzer = pdfalyzer
        self.yaralyzer = get_file_yaralyzer(self.pdfalyzer.pdf_path)

    def print_everything(self) -> None:
        """Print every kind of analysis on offer to Rich console."""
        self.print_document_info()
        self.print_summary()
        self.print_tree()
        self.print_rich_table_tree()
        self.print_font_info()
        self.print_non_tree_relationships()

    def print_document_info(self) -> None:
        """Print the embedded document info (author, timestamps, version, etc)."""
        print_section_header(f'Document Info for {self.pdfalyzer.pdf_basename}')
        console.print(pp.pformat(self.pdfalyzer.pdf_reader.getDocumentInfo()))
        console.line()
        console.print(bytes_hashes_table(self.pdfalyzer.pdf_bytes, self.pdfalyzer.pdf_basename))
        console.line()
        console.print(self._stream_objects_table())
        console.line()

    def print_tree(self) -> None:
        """Print the simple view of the PDF tree."""
        print_section_header(f'Simple tree view of {self.pdfalyzer.pdf_basename}')

        for pre, _fill, node in RenderTree(self.pdfalyzer.pdf_tree, style=DoubleStyle):
            if isinstance(node, SymlinkNode):
                symlink_rep = get_symlink_representation(node.parent, node)
                console.print(pre + f"[{symlink_rep.style}]{symlink_rep.text}[/{symlink_rep.style}]")
            else:
                console.print(Text(pre) + node.__rich__())

        self.pdfalyzer._verify_all_nodes_encountered_are_in_tree()
        console.print("\n\n")

    def print_rich_table_tree(self) -> None:
        """Print the rich view of the PDF tree."""
        print_section_header(f'Rich tree view of {self.pdfalyzer.pdf_basename}')
        console.print(generate_rich_tree(self.pdfalyzer.pdf_tree))
        self.pdfalyzer._verify_all_nodes_encountered_are_in_tree()

    def print_summary(self) -> None:
        print_section_header(f'PDF Node Summary for {self.pdfalyzer.pdf_basename}')
        console.print_json(data=self._analyze_tree(), sort_keys=True)

    def print_font_info(self, font_idnum=None) -> None:
        print_section_header(f'{len(self.pdfalyzer.font_infos)} fonts found in {self.pdfalyzer.pdf_basename}')

        for font_info in [fi for fi in self.pdfalyzer.font_infos if font_idnum is None or font_idnum == fi.idnum]:
            font_info.print_summary()

    def print_streams_analysis(self, idnum: Optional[int] = None) -> None:
        print_section_header(f'Binary Stream Analysis / Extraction')
        console.print(self._stream_objects_table())

        for node in [n for n in self.pdfalyzer.stream_nodes() if idnum is None or idnum == n.idnum]:
            node_stream_bytes = node.stream_data

            if node_stream_bytes is None or node.stream_length == 0:
                print_section_sub_subheader(f"{node} stream has length 0", style='dim')
                continue

            if not isinstance(node_stream_bytes, bytes):
                msg = f"Stream in {node} is not bytes, it's {type(node.stream_data)}. Will reencode for YARA " + \
                       "but they may not be the same bytes as the original stream!"
                log.warning(msg)
                node_stream_bytes = node_stream_bytes.encode()

            print_section_subheader(f"{escape(str(node))} Summary and Analysis", style=f"{BYTES_HIGHLIGHT} reverse")
            binary_scanner = BinaryScanner(node_stream_bytes, node)
            console.print(bytes_hashes_table(binary_scanner.bytes))
            binary_scanner.print_stream_preview()
            binary_scanner.check_for_dangerous_instructions()

            if not YaralyzerConfig.SUPPRESS_DECODES:
                binary_scanner.check_for_boms()
                binary_scanner.force_decode_all_quoted_bytes()

            binary_scanner.print_decoding_stats_table()

    def print_yara_results(self) -> None:
        print_section_header(f"YARA Scan of PDF rules for '{self.pdfalyzer.pdf_basename}'")
        self.yaralyzer.yaralyze()
        console.line(2)

        for node in self.pdfalyzer.stream_nodes():
            if node.stream_length == DECODE_FAILURE_LEN:
                log.warning(f"{node} binary stream could not be extracted")
            elif node.stream_length == 0 or node.stream_data is None:
                log.debug(f"No binary to scan for {node}")
            else:
                get_bytes_yaralyzer(node.stream_data, str(node)).yaralyze()
                console.line(2)

    def print_non_tree_relationships(self) -> None:
        """Print the inter-node, non-tree relationships for all nodes in the tree"""
        console.line(2)
        console.print(Panel(f"Other Relationships", expand=False), style='reverse')

        for node in LevelOrderIter(self.pdfalyzer.pdf_tree):
            if len(node.non_tree_relationships) == 0:
                continue

            console.print("\n")
            console.print(Panel(f"Non tree relationships for {node}", expand=False))
            node.print_non_tree_relationships()

    def _analyze_tree(self) -> dict:
        """Generate a dict with some basic data points about the PDF tree"""
        pdf_object_types = defaultdict(int)
        node_labels = defaultdict(int)
        keys_encountered = defaultdict(int)
        node_count = 0

        for node in self.pdfalyzer.node_iterator():
            pdf_object_types[type(node.obj).__name__] += 1
            node_labels[node.label] += 1
            node_count += 1

            if isinstance(node.obj, dict):
                for k in node.obj.keys():
                    keys_encountered[k] += 1

        return {
            'keys_encountered': keys_encountered,
            'node_count': node_count,
            'node_labels': node_labels,
            'pdf_object_types': pdf_object_types,
        }

    def _stream_objects_table(self) -> Table:
        return stream_objects_table(self.pdfalyzer.stream_nodes())
