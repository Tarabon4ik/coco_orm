# coco_orm

coco_orm is an ORM built to simplify working with datasets in COCO format.
 
## Installation

`pip install coco-orm`

## Examples

### Create a new annotations file and fill it with data in COCO format:

    from coco_orm import CocoDataset
    from coco_orm.models import Image, Category, Annotation

    # create an annotations.json file containing COCO dataset annotations.
    coco_dataset = CocoDataset(".../dataset/annotations.json")
    
    # create a new image
    image = Image(id=1, file_name="01.jpg", width=320, height=320)
    coco_dataset.images.append(image)

    # create a new category
    category = Category(id=1, name="cat")
    coco_dataset.categories.append(category)

    # create a new annotation
    annotation = Annotation(image_id=1, category_id=1, bbox=[260, 177, 231, 199])
    coco_dataset.annotations.append(annotation)

    # save to the .json file
    coco_dataset.save()


### Apply filters to the COCO dataset collections

    from coco_orm import CocoDataset
    from coco_orm.filters import ImageFilters

    # read annotations file
    coco_dataset = CocoDataset(".../dataset/annotations.json")

    # filter an image collection by ids
    image_filters = (ImageFilters().ids([1, 3]))
    coco_dataset.images.filter(image_filters, inplace=True)

    # save filtered dataset to the separate file
    coco_dataset.save(".../dataset/filtered_annotations.json")

## Further info
Created by a team of Computer Vision enjoyers of Igor Sikorsky Kyiv Polytechnic Institute.

## Support Ukraine - Stop the War
Since 20 February 2014 Ukraine has been facing Russian military aggression that has left over 14 000 people killed and over 30 000 injured. Your support is crucial as it helps Ukrainian people to stand against Russian aggression.

[We are fighting for the future without tyranny.](https://war.ukraine.ua/support-ukraine/)
[<img src="https://www.nhc.nl/assets/uploads/2022/02/shutterstock_2125795721-1-scaled-e1645609704346.jpg">](https://war.ukraine.ua/support-ukraine/)
