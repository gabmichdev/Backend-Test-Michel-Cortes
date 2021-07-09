from typing import List
import logging
from collections import defaultdict
from datetime import datetime

from django.urls import reverse

from backend_test.envtools import getenv
from core.utils.slack_client import SlackRESTClient
from core.utils.date_utils import generate_day_range_for_date


logger = logging.getLogger("backend_test")

CONVERSATION_NAME = getenv(
    "CONVERSATION_NAME", default="cornershop-backend-test"
).lower()
TOKEN = getenv("SLACK_BOT_TOKEN", default="No token")
client = SlackRESTClient(TOKEN)


def detail_url(menu_id):
    """Return menu detail URL"""
    return reverse("menu:menu-detail", args=[menu_id])


def send_todays_menu_to_slack():

    from core.models import Menu
    from django.contrib.sites.models import Site

    # Retrieve menus for today
    try:
        now = datetime.now()
        gte, lte = generate_day_range_for_date(now)
        menus_found = Menu.objects.filter(
            preparation_date__gte=gte,
            preparation_date__lte=lte,
        )

        def get_menu_message(menus: List[Menu]):
            """Function that will create message from the menus"""
            # Set weekday name
            weekday_name = ""
            output_message = """
        Menu de hoy %s:\n"""
            weekday_name = Menu._get_human_readable_value(
                now.isoweekday(), "DOW_CHOICES"
            ).lower()
            output_message = output_message.replace("%s", weekday_name)

            # Store the meal time keys and menus
            # {
            #     'Opcion para {meal_time_name}': ['Menu1', 'Menu2']
            # }
            meal_time_menus = defaultdict(list)
            for menu in menus:
                # Get name of meal instead of 1, 2, 3, etc.
                meal_time_name = Menu._get_human_readable_value(
                    menu.meal_time, "MEAL_TIMES"
                ).lower()
                meal_message = f"Opciones para {meal_time_name}"
                menu_url = detail_url(menu.id)
                site_url = Site.objects.get_current().domain
                full_url = "https://%s%s" % (site_url, menu_url)
                # Build menu string
                menu_string = str(menu)
                menu_string += f"Revisa este menu!: {full_url}"
                meal_time_menus[meal_message].append(menu_string)

            # Parse the menu options string
            for meal_message, meal_menus in meal_time_menus.items():
                output_message += f"{meal_message}:\n"
                for i, meal_menu in enumerate(meal_menus, 1):
                    meal_menu = meal_menu.replace("%s", str(i))
                    output_message += f"\t{meal_menu}\n"
            return output_message

        if len(menus_found) > 0:

            output_message = get_menu_message(menus_found)
        else:
            output_message = "El dia de hoy no hay menus, una disculpa."
        output_message += f"\nQue tengas excelente dia!"
        logger.info(str(output_message))
        # Send message to slack
        conversation_id = client.get_slack_conversation(CONVERSATION_NAME)
        client.send_slack_message(conversation_id, output_message)
    except Exception as e:
        logger.error(str(e))
