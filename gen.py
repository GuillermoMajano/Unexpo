import os
import cairosvg
from typing import List


class GenImages:
    def __init__(self, svg_src: str) -> None:
        self.svg_src = svg_src
        self._svg_cache = None  # Cache for SVG content

    def __get_svg(self) -> str:
        """
        Reads the SVG file and returns its contents as a string with caching.
        
        :return: str: SVG file contents
        """
        if self._svg_cache is None:
            with open(self.svg_src, "r", encoding="utf-8") as file:
                self._svg_cache = file.read()
        return self._svg_cache

    def replace_colors(self, color_: str, original_color: str = "#0063be") -> str:
        """
        Replaces the default color of the SVG with the specified color.
        
        :param color_: str: The color to replace the default color with
        :param original_color: str: The color to be replaced (default: "#0063be")
        :return: str: The SVG file contents with the default color replaced
        """
        return self.__get_svg().replace(original_color, color_)

    def save(
        self,
        foreground_color: str,
        output: str,
        output_width: int,
        ext: str = "png",
        background_color: str = None
    ) -> None:
        """
        Saves the SVG image with the specified foreground color and dimensions.
        
        :param foreground_color: str: The color to replace the default color with
        :param output: str: The output file path
        :param output_width: int: The width of the output image
        :param ext: str: The output file extension (default: png)
        :param background_color: str: Optional background color for the image
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output) or os.path.dirname(output), exist_ok=True)

        # Convert SVG to PNG
        png_data = cairosvg.svg2png(
            bytestring=self.replace_colors(foreground_color),
            output_width=output_width,
            scale=1,
            background_color= background_color
        )

        # Save the image directly without loading into PIL unless needed
        output_path = f"{output}.{ext}"
        with open(output_path, "wb") as f:
            f.write(png_data)


def write_readme(directory: str, image_files: List[str]) -> None:
    """
    Generates a README.md file with a table of all logo variations.
    
    :param directory: str: Directory where README will be saved
    :param image_files: List[str]: List of image file paths to include
    """
    base_url = "https://github.com/unexpo-poz/brand/blob/main/logo/icon/"
    content = """\
<h1 align="center">
    <a href="http://www.poz.unexpo.edu.ve"><img src="https://github.com/unexpo-poz/brand/blob/main/logo/standar/primary-2048.png" width="175px" alt="UNEXPO"></a>
</h1>
 
<h3 align="center">La Universidad Tecnica del Estado Venezolano.</h3>


[Regresar al directorio raiz](https://github.com/unexpo-poz/brand)

## Logos

### Nota 
Si algun logo no se visualiza correctamente, intenta cambiar el tema de Github de claro a oscuro o viceversa.

| Vista | Tamaño | Uso |
|-------|--------|-----|
"""

    for image_file in image_files:
        file_name = os.path.basename(image_file)
        size = file_name.split('-')[-1].split('.')[0]
        file_url = f"{base_url}{file_name}?raw=true"
        content += f"|<img src='{file_url}' width='64' alt=''/> | {size}px | ✅ | [{file_name}](https://github.com/unexpo-poz/brand/blob/main/logo/icon/{file_name}) |\n"

    readme_path = os.path.join(directory, "README.md")
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(content)


def generate_logos(gen: GenImages) -> List[str]:
    """
    Generates all logo variations based on predefined colors and sizes.
    
    :param gen: GenImages: Instance of GenImages class
    :return: List[str]: List of generated file paths
    """
    COLOR_MAPPING = {
        "#FFF": "white",
        "#000": "black",
        "#0063BE": "primary",
        "#3E78B2": "secondary",
        "#454647": "dark",
        "#EBEBEB": "light"
    }
    
    colors = ["#454647", "#EBEBEB", "#FFF", "#000", "#0063BE", "#3E78B2"]
    sizes = [16, 32, 64, 100, 128, 512, 1024, 2048]
    generated_files = []

    for color in colors:
        color_type = COLOR_MAPPING[color]
        
        for size in sizes:
            # Favicons (only primary color in small sizes)
            if size <= 128 and color == "#0063BE":
                output_path = f"logo/favicon/favicon-{size}"
                gen.save(color, output_path, size, ext="png")
                generated_files.append(f"{output_path}.png")
            
            if size >= 512:
                # Standard version
                output_path = f"logo/standar/{color_type}-{size}"
                gen.save(color, output_path, size)
                generated_files.append(f"{output_path}.png")
                

    return generated_files


def main():
    svg_path = "./logo/asset-svg/logo.svg"
    gen = GenImages(svg_path)
    
    generated_files = generate_logos(gen)
    write_readme("./", generated_files)
    
    print("Logo images generated successfully!")


if __name__ == "__main__":
    main()