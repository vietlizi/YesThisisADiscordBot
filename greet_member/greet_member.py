from PIL import Image, ImageDraw, ImageFont
import io

def generate_greeting_card(member_name, member_discriminator, member_count, background_path, font_path):
    background = Image.open(background_path).convert("RGBA")
    overlay = Image.new("RGBA", background.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_name = ImageFont.truetype(font_path, 50)
    font_member = ImageFont.truetype(font_path, 30)
    name_text = f"{member_name}#{member_discriminator}"
    welcome_text = "just joined the server"
    member_number = f"Member #{member_count}"

    width, height = background.size
    name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    welcome_bbox = draw.textbbox((0, 0), welcome_text, font=font_member)
    member_bbox = draw.textbbox((0, 0), member_number, font=font_member)

    name_pos = ((width - (name_bbox[2] - name_bbox[0])) // 2, height // 2 - 50)
    welcome_pos = ((width - (welcome_bbox[2] - welcome_bbox[0])) // 2, height // 2 + 20)
    member_pos = ((width - (member_bbox[2] - member_bbox[0])) // 2, height // 2 + 60)

    draw.text(name_pos, name_text, font=font_name, fill="white")
    draw.text(welcome_pos, welcome_text, font=font_member, fill="white")
    draw.text(member_pos, member_number, font=font_member, fill="white")

    combined = Image.alpha_composite(background, overlay)
    buffer = io.BytesIO()
    combined.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
