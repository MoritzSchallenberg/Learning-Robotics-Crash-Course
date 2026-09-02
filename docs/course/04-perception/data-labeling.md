# Data labeling

{{ common }}

{{ advanced }} **Status: advanced reading.** Needed only if you train a
[custom YOLO model](object-detection.md#training-a-custom-model) — not part
of [module 4](index.md)'s core task.

## 1. Collect images

Take **at least 30** photographs of the object, and vary everything:
distance, angle, lighting, background, occlusion. A model trained on 200
identical photos will only recognise that exact photo.

## 2. Label them

Use any labelling tool — [MakeSense.ai](https://www.makesense.ai/) runs in
the browser and needs no account; [Roboflow](https://roboflow.com/) and
[CVAT](https://www.cvat.ai/) manage larger team datasets.

Draw a box around each object and export in **YOLO format**.

:::{warning}
Draw the box tightly around the object's actual boundary. Loose boxes teach
the model that the surrounding background is part of the object, and
detection accuracy collapses. If an image is blurred, estimate the true
extent rather than guessing generously.

{{ carologistics }} The Carologistics team's specific labeling rules for
conveyors, slides and workpieces are on the
[Carologistics/Robotino platform page](../../platforms/carologistics-robotino.md#data-labeling) —
this page covers the general workflow; that page covers what "tight" means
for their specific objects.
:::

## 3. Organise the dataset

```text
my_model/
└── dataset/
    ├── images/
    │   ├── train/     ~80% of your images
    │   └── val/       ~20%, used to check the model during training
    └── labels/
        ├── train/
        └── val/
```

## 4. Write the configuration and train

See [Training a custom model](object-detection.md#training-a-custom-model)
for the `dataset.yaml` and the `yolo train` command.

## Common mistakes

**Training and validation images overlap or are near-duplicates.** The
model appears to work in `runs/detect/train` and fails on anything new.

**All images taken in one session, one lighting condition.** The model
learns the lighting, not the object.

**Boxes drawn loosely "to be safe."** The opposite of safe — see the warning
above.

## Further reading

- [MakeSense.ai](https://www.makesense.ai/) · [Roboflow](https://roboflow.com/) ·
  [CVAT](https://www.cvat.ai/)
- Back to [module 4](index.md) · [object detection](object-detection.md)
