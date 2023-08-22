import random
from pathlib import Path
from PIL import Image, ImageDraw

FILE_NAME = 'D:/lol.jpg'
NOISE_FACTOR = 35
FILTER_COUNT = 3

def gr(draw, width, height, pixel):
	for i in range(width):
		for j in range(height):
			r = pixel[i, j][0]
			g = pixel[i, j][1]
			b = pixel[i, j][2]
			average = (b + g + b) // 3
			draw.point((i, j), (average, average, average))

def noise(draw, width, height):  #зашумление
	pixelsCount = int(width * height * NOISE_FACTOR / 100)
	for i in range(pixelsCount):
		noiseValue = random.randint(0, 1) * 255
		width1 = random.randint(0, width - 1)
		height1 = random.randint(0, height - 1)
		draw.point((width1, height1), (noiseValue, noiseValue, noiseValue))

def linearFilter(draw, width, height, pixel):  #линейный фильтр
	crossFilter = [()] * 5
	for i in range(width):      #построчно очищаем изображение от шума
		for j in range(height):

			if width - i < 5 and height - j < 1:   
				crossFilter[0] = pixel[width - 5, height]
				crossFilter[1] = pixel[width - 4, height]
				crossFilter[2] = pixel[width - 3, height]
				crossFilter[3] = pixel[width - 2, height]
				crossFilter[4] = pixel[width -1 , height]

			elif width - i < 5:

				crossFilter[0] = pixel[width - 5, j]
				crossFilter[1] = pixel[width - 4, j]
				crossFilter[2] = pixel[width - 3, j]
				crossFilter[3] = pixel[width - 2, j]
				crossFilter[4] = pixel[width-1 , j]

			
			elif height - j < 1:

				crossFilter[0] = pixel[i, height]
				crossFilter[1] = pixel[i + 1, height]
				crossFilter[2] = pixel[i + 2, height]
				crossFilter[3] = pixel[i + 3, height]
				crossFilter[4] = pixel[i + 4, height]

			else:
				crossFilter[0] = pixel[i, j]
				crossFilter[1] = pixel[i+1, j]
				crossFilter[2] = pixel[i+2, j]
				crossFilter[3] = pixel[i+3,  j]
				crossFilter[4] = pixel[i+4,  j]

			crossFilter.sort()
			pixel[i, j] = crossFilter[2]
			draw.point((i, j), (pixel[i, j][0], pixel[i, j][1], pixel[i, j][2]))

def main():
	object_name = FILE_NAME.split("/")[1]
	print(object_name)
	cur_dir = Path.cwd()
	print(cur_dir)
	res_dir = cur_dir / 'res1' #сохраняем все получившиеся изображения в папку res1
	print(res_dir)
	Path(res_dir).mkdir(parents=False, exist_ok=True)
	res_dir = str(res_dir) + "/"
	print(res_dir)

	image = Image.open(FILE_NAME)
	draw = ImageDraw.Draw(image)
	width = image.size[0]
	height = image.size[1]
	pix = image.load()
	gr(draw, width, height, pix)
	image.save(res_dir + "gray.jpg", "JPEG") #сохраняем изображение, перекрашенное в серый

	
	noise(draw, width, height)
	image.save(res_dir + str(NOISE_FACTOR) + "_digital_noise.jpg", "JPEG") #сохраняем зашумленное изображение
	for i in range(FILTER_COUNT):
			linearFilter(draw, width, height, pix)
			image.save(res_dir + str(NOISE_FACTOR) + "_digital_noise_" + str(i+1) + "_cross_filter.jpg", "JPEG") #сохраняем результат работы фильтра для каждой итерации


if __name__ == '__main__':
	main()