"""Task1, Task2."""
# ruff: noqa: PTH123, T203
from __future__ import annotations

from pprint import pprint
from typing import TypeAlias, TypedDict


class Ingredient(TypedDict):
    """Typed dict class for ingredient."""

    ingredient_name: str
    quantity: int
    measure: str


CookBook: TypeAlias = dict[str, list[Ingredient]]


def get_raw_recipes(file_path: str) -> list[str]:
    """Read file content from `file_path` and return it."""
    with open(file_path) as file:
        return file.readlines()


def parse_recipes(raw_text: list[str]) -> CookBook:
    """Parse recipes from `raw_text` to extract information about the recipes and their respective ingredients."""
    result: CookBook = {}
    current_recipe = None
    i = 0
    while i < len(raw_text):
        line = raw_text[i].strip()
        if line:
            if not current_recipe:
                current_recipe = line
                result[current_recipe] = []
            elif "|" not in line:
                i += 1
                continue
            else:
                ingredient_name, quantity, measure = line.split(" | ")
                ingredient_dict = {
                    "ingredient_name": ingredient_name,
                    "quantity": int(quantity),
                    "measure": measure,
                }
                result[current_recipe].append(ingredient_dict)
        else:
            current_recipe = None
        i += 1
    return result


def get_shop_list_by_dishes(
    dishes: list[str],
    person_count: int,
    cook_book: CookBook,
) -> dict[str, dict]:
    """Generate ingredient list required to cook the specified `dishes` for the given `person_count`."""
    shop_list: dict[str, dict] = {}
    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient["ingredient_name"]
                quantity = ingredient["quantity"] * person_count
                measure = ingredient["measure"]
                if name in shop_list:
                    shop_list[name]["quantity"] += quantity
                else:
                    shop_list[name] = {"quantity": quantity, "measure": measure}
    return shop_list


if __name__ == "__main__":
    file_name = "recipes.txt"
    recipes = get_raw_recipes(file_name)
    cookbook = parse_recipes(recipes)

    pprint(
        get_shop_list_by_dishes(["Запеченный картофель", "Омлет"], 2, cookbook),
    )
