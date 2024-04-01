import random

# 集装箱的尺寸
CONTAINER_WIDTH = 2.5  # 宽度
CONTAINER_LENGTH = 12.5  # 长度
CONTAINER_HEIGHT = 2.6  # 高度

# 船上的集装箱层数
LAYERS = 5

# 每层集装箱的数量（逐层递减）
CONTAINERS_PER_LAYER = [48, 48, 47, 46, 45]

# 集装箱之间的最小间距
SPACING = 1.5

# 船高
ShipHigh = 25
# 船的边界范围
SHIP_BOUNDARY_X_MIN = 255
SHIP_BOUNDARY_X_MAX = 455
SHIP_BOUNDARY_Y_MIN = 70
SHIP_BOUNDARY_Y_MAX = 130

# 生成集装箱坐标的函数
def generate_container_positions(layers, containers_per_layer, ship_boundary_x, ship_boundary_y, container_size,
                                 spacing):
    positions = []
    current_y = ship_boundary_y[0] + SPACING  # Start from the minimum Y boundary with spacing

    for layer in range(layers):
        current_x = ship_boundary_x[0] + SPACING  # Start from the minimum X boundary with spacing
        for _ in range(containers_per_layer[layer]):
            # Check if the next container fits horizontally
            if current_x + container_size[0] + SPACING > ship_boundary_x[1]:
                break  # No more containers fit on this layer

            # position_x 被赋予一个在 current_x 和 min(current_x + container_size[0],
            # ship_boundary_x[1] - SPACING) 之间的随机值。这样做是为了在每个可能的X位置上稍微随机化箱子的位置，而不是让它们严格按照一个固定的网格来排列。
            # 这样做可以增加一点真实感，因为在现实中，箱子的放置位置可能不会完美对齐。
            position_x = random.uniform(current_x + container_size[0] + SPACING
                                        , min(current_x + 2 * container_size[0] + SPACING, ship_boundary_x[1] - SPACING))
            # position_x = current_x + container_size[0]
            # The Y position is fixed for each layer
            position_y = current_y

            # The Z position is based on the layer height
            position_z = layer * CONTAINER_HEIGHT + ShipHigh

            positions.append((position_x, position_y, position_z))

            # Move to the next horizontal position+
            current_x += container_size[0] + spacing

            # Move to the next vertical position
        current_y += container_size[1] + spacing

        # # Check if the next layer fits vertically
        # if current_y + container_size[1] + SPACING > ship_boundary_y[1]:
        #     break  # No more layers fit on the ship

    return positions


# Generate container positions within the ship boundaries
unload_positions = generate_container_positions(
    LAYERS,
    CONTAINERS_PER_LAYER,
    (SHIP_BOUNDARY_X_MIN, SHIP_BOUNDARY_X_MAX),
    (SHIP_BOUNDARY_Y_MIN, SHIP_BOUNDARY_Y_MAX),
    (CONTAINER_WIDTH, CONTAINER_LENGTH),
    SPACING
)

# Convert coordinates to the specified format and print
formatted_positions = [(round(pos[0], 1), round(pos[1], 1), round(pos[2], 1)) for pos in unload_positions]
print("unload_positions = [")
for pos in formatted_positions:
    print(f"    {pos},")
print("]")
