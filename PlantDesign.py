import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

def layout_flowline(factory_w, factory_h, machines, margin=1.0, aisle=1.5, row_gap=2.0):
    """
    Simple flow-line / shelf layout.
    machines = list of dict: [{"id":1, "w":3, "h":2}, ...] in precedence order
    Returns list with placed positions: [{"id":..,"x":..,"y":..,"w":..,"h":..}, ...]
    """
    placed = []
    x = margin
    y = margin
    current_row_height = 0.0

    for m in machines:
        w, h = m["w"], m["h"]

        # if doesn't fit in current row, move to next row
        if x + w + margin > factory_w:
            x = margin
            y += current_row_height + row_gap
            current_row_height = 0.0

        # if doesn't fit vertically, fail
        if y + h + margin > factory_h:
            raise ValueError(f"Not enough space to place machine {m['id']} within the factory area.")

        placed.append({"id": m["id"], "x": x, "y": y, "w": w, "h": h})
        x += w + aisle
        current_row_height = max(current_row_height, h)

    return placed

def draw_factory_plan(factory_w, factory_h, placed, out_png="factory_plan.png", title="Factory Layout Plan"):
    fig, ax = plt.subplots(figsize=(10, 6))

    # factory boundary
    ax.add_patch(Rectangle((0, 0), factory_w, factory_h, fill=False, linewidth=2))
    ax.set_xlim(-1, factory_w + 1)
    ax.set_ylim(-1, factory_h + 1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title)

    # draw machines
    centers = []
    for p in placed:
        rect = Rectangle((p["x"], p["y"]), p["w"], p["h"], fill=False, linewidth=2)
        ax.add_patch(rect)
        cx = p["x"] + p["w"] / 2
        cy = p["y"] + p["h"] / 2
        centers.append((p["id"], cx, cy))
        ax.text(cx, cy, f"M{p['id']}", ha="center", va="center", fontsize=11)

        # show size
        ax.text(p["x"], p["y"] - 0.4, f"{p['w']}×{p['h']}", ha="left", va="top", fontsize=9)

    # draw flow arrows (1->2->... based on order in placed list)
    for i in range(len(centers) - 1):
        _, x1, y1 = centers[i]
        _, x2, y2 = centers[i + 1]
        arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=15)
        ax.add_patch(arrow)

    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Length (m)")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.show()
    return out_png

# -------------------------
# EXAMPLE INPUT (แก้ตรงนี้)
# -------------------------
factory_w, factory_h = 30, 18  # พื้นที่โรงงาน (เมตร)

machines = [
    {"id": 1, "w": 4, "h": 3},
    {"id": 2, "w": 5, "h": 3},
    {"id": 3, "w": 6, "h": 3},
    {"id": 4, "w": 4, "h": 4},
    {"id": 5, "w": 5, "h": 3},
    {"id": 6, "w": 4, "h": 3},
    {"id": 7, "w": 6, "h": 3},
    {"id": 8, "w": 4, "h": 3},
    {"id": 9, "w": 5, "h": 4},
    {"id": 10, "w": 4, "h": 3},
]

placed = layout_flowline(factory_w, factory_h, machines, margin=1.0, aisle=1.5, row_gap=2.0)
png = draw_factory_plan(factory_w, factory_h, placed, out_png="factory_plan.png",
                        title="Factory Layout (Flow line 1→10)")
print("Saved:", png)