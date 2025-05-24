import sys
import re

HTML_PATH = "docs/portfolio.html"

def update_filter(filter_class, filter_name=None, action="add"):
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Find the filter button group
    pattern = r'(<div class="button-group.*?id="filters">)(.*?)(</div>)'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        print("Filter button group not found.")
        return

    before, filters_html, after = match.groups()

    if action == "add":
        filter_tag = f'<a class="text-decoration-none text-uppercase" data-filter=".{filter_class}" href="#">{filter_name}</a>'
        # Check if a filter with the same data-filter already exists
        data_filter_pattern = rf'<a[^>]*data-filter="\.[^"]*{re.escape(filter_class)}[^"]*"[^>]*>.*?</a>'
        if re.search(data_filter_pattern, filters_html):
            print(f"A filter with data-filter='.{filter_class}' already exists.")
            return
        filters_html = filters_html.strip() + "\n" + filter_tag + "\n"
    elif action == "remove":
        # Remove any <a> that contains the data-filter attribute with the given value
        filters_html = re.sub(
            rf'\s*<a[^>]*data-filter="\.{re.escape(filter_class)}"[^>]*>.*?</a>\s*',
            '',
            filters_html,
            flags=re.MULTILINE
        )
    else:
        print("Unknown action. Use 'add' or 'remove'.")
        return

    # Rebuild the HTML
    new_html = html[:match.start(2)] + filters_html + html[match.end(2):]
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Filter {'added' if action == 'add' else 'removed'} successfully.")

if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[3] == "add":
        update_filter(sys.argv[1], sys.argv[2], "add")
    elif len(sys.argv) == 3 and sys.argv[2] == "remove":
        update_filter(sys.argv[1], action="remove")
    else:
        print("Usage for add: python add_remove_filter.py <class> <name> add")
        print("Usage for remove: python add_remove_filter.py <class> remove")
        print('Example add: python add_remove_filter.py test "Test Filter" add')
        print('Example remove: python add_remove_filter.py test remove')
        sys.exit(1)