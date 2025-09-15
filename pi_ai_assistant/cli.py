import sys
from typing import Optional

import click
from rich.console import Console

from .config import AppConfig, load_config, PrinterConfig, KlipperConfig, write_printer_and_klipper_to_config
from .providers.factory import create_provider
from .moonraker import test_moonraker_connection

console = Console()


@click.group(invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("query", required=False)
@click.option("--backend", type=click.Choice(["huggingface"]), help="Override backend")
@click.option("--model", type=str, help="Override model name")
@click.option("--temperature", type=float, help="Sampling temperature override")
@click.option("--max-tokens", type=int, help="Max tokens override")
@click.option("--repl", is_flag=True, help="Start interactive REPL mode")
@click.pass_context
def main(
	ctx: click.Context,
	query: Optional[str],
	backend: Optional[str],
	model: Optional[str],
	temperature: Optional[float],
	max_tokens: Optional[int],
	repl: bool,
) -> None:
	"""Cloud-only CLI AI assistant (Hugging Face Inference API)."""
	config = load_config(
		backend_override=backend,
		model_override=model,
		temperature_override=temperature,
		max_tokens_override=max_tokens,
	)
	ctx.obj = config

	if not config.hf_token:
		console.print("[yellow]Set HF_TOKEN env var or add hf_token to config.toml[/]")

	if ctx.invoked_subcommand is not None:
		return

	if repl and not query:
		sys.exit(_run_repl(config))
	if query:
		sys.exit(_run_single_query(config, query))
	console.print("[yellow]No query provided. Starting REPL...[/]")
	sys.exit(_run_repl(config))


def _run_single_query(config: AppConfig, prompt: str) -> int:
	provider = create_provider(config)
	response = provider.generate(prompt)
	console.print(response)
	return 0


def _run_repl(config: AppConfig) -> int:
	provider = create_provider(config)
	console.print("[bold green]Pi Assistant REPL[/] — type 'exit' or Ctrl-D to quit")
	while True:
		try:
			prompt = console.input("[bold cyan]> [/]")
		except (EOFError, KeyboardInterrupt):
			console.print()
			break
		if not prompt:
			continue
		if prompt.strip().lower() in {"exit", "quit"}:
			break
		response = provider.generate(prompt)
		console.print(response)
	return 0


@main.command("setup")
@click.option("--make", "make_", prompt=True, help="Printer make (e.g., Prusa, Creality)")
@click.option("--model", prompt=True, help="Printer model (e.g., MK3S, Ender 3)")
@click.option("--bed-width", type=float, prompt=True, help="Bed width in mm")
@click.option("--bed-depth", type=float, prompt=True, help="Bed depth in mm")
@click.option("--origin-x", type=float, default=0.0, show_default=True, prompt=True, help="Origin X in mm")
@click.option("--origin-y", type=float, default=0.0, show_default=True, prompt=True, help="Origin Y in mm")
@click.option(
	"--kinematics",
	type=click.Choice(["cartesian", "corexy", "delta", "bedslinger", "scara", "other"], case_sensitive=False),
	prompt=True,
	help="Printer kinematics",
)
@click.option("--moonraker-url", default=None, help="Moonraker base URL (defaults to localhost:7125)")
@click.option("--api-key", default=None, help="Moonraker API key if required")
@click.pass_obj
def setup_cmd(config: AppConfig, make_: str, model: str, bed_width: float, bed_depth: float, origin_x: float, origin_y: float, kinematics: str, moonraker_url: Optional[str], api_key: Optional[str]) -> None:
	printer = PrinterConfig(
		make=make_,
		model=model,
		bed_width_mm=bed_width,
		bed_depth_mm=bed_depth,
		origin_x_mm=origin_x,
		origin_y_mm=origin_y,
		kinematics=kinematics.lower(),
	)
	moon_url = moonraker_url or config.klipper.moonraker_url
	klipper = KlipperConfig(moonraker_url=moon_url, api_key=api_key or config.klipper.api_key)
	ok, _ = test_moonraker_connection(klipper)
	if not ok:
		console.print("[yellow]Moonraker not reachable at default URL. Let's set it.[/]")
		moon_url = click.prompt("Moonraker URL", default=config.klipper.moonraker_url)
		klipper = KlipperConfig(moonraker_url=moon_url, api_key=api_key or config.klipper.api_key)

	write_printer_and_klipper_to_config(printer, klipper)
	console.print("[green]Saved printer and Klipper settings.[/]")


if __name__ == "__main__":
	main()
