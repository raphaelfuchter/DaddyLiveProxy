import reflex as rx
import json
from ..step_daddy import StepDaddy

class ApiScheduleState(rx.State):
    schedule_json: str = "Carregando..."

    async def load_schedule(self):
        try:
            daddy = StepDaddy()
            schedule_data = await daddy.schedule()
            self.schedule_json = json.dumps(schedule_data, indent=4)
        except Exception as e:
            self.schedule_json = json.dumps({"error": str(e)})

@rx.page(route="/api/schedule", on_load=ApiScheduleState.load_schedule)
def api_schedule_page() -> rx.Component:
    """Uma página que exibe o conteúdo JSON num bloco de código."""
    return rx.code_block(
        ApiScheduleState.schedule_json,
        language="json",
        show_line_numbers=True,
    )