def recognize_hand_cards(model, region, id_to_card):
    time.sleep(1)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
    screenshot_image.save("a.jpg")
    
    results = model(screenshot_image, conf=0.8)
    for result in results:
        detected_items = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        sorted_indices = np.argsort([item[0] for item in detected_items])[:14]
        hand_ids = [int(class_ids[index]) for index in sorted_indices]
        hand = [id_to_card.get(id, "") for id in hand_ids]
    return hand, detected_items[sorted_indices]