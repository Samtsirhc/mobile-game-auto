dorm_order = 0
    switch_state = 0    # 换班状态，0：在找宿舍；1：在换干员
    switch_step = 0
    while True:
        # 找宿舍
        if dorm_order < 3 and switch_state == 0:
            emulator.swipe((1216, 650, 1215, 300))
            time.sleep(1)
            emulator.find_and_click(f'宿舍', (236, 51))
            if emulator.find_img(f'在换班'):
                switch_state = 1
                dorm_order += 1
                pass
        if dorm_order == 3 and switch_state == 0:
            emulator.swipe((1216, 650, 1215, 158))
            time.sleep(1)
            emulator.find_and_click(f'B4宿舍', (236, 101))
            if emulator.find_img(f'在换班'):
                switch_state = 1
                dorm_order += 1
                pass

        # 安排干员休息
        if switch_state == 1:
            if switch_step < 3:
                emulator.find_and_click(f'清空选择')
                switch_step += 1
            if switch_step == 3:
                for _ in range(5):
                    time.sleep(0.1)
                    emulator.click((1053, 47))
                switch_step += 1
                time.sleep(1)
            if switch_step == 4:
                if emulator.find_img('心情上'):
                    switch_step += 1
                else:
                    emulator.click((1053, 47))
                    time.sleep(0.5)
            if switch_step == 5:
                for wife_x in range(5):
                    for wife_y in range(2):
                        emulator.click(
                            (487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.1)
                switch_step += 1
            if switch_step == 6:
                emulator.find_and_click(['确认','红底白勾'])
                if emulator.find_img(f'在进驻总览'):
                    switch_step = 0
                    switch_state = 0

        # 干员上班
        if dorm_order > 3 and switch_state == 0:
            if switch_step == 0:
                emulator.find_and_click('干员空位', (10, 28))
                if emulator.find_img(f'在换班'):
                    switch_step += 1

            if switch_step == 1:
                for wife_x in range(3):
                    for wife_y in range(2):
                        emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.7)
                switch_step += 1

            if switch_step == 2:
                emulator.find_and_click(['确认','红底白勾'])
                if emulator.find_img(f'在进驻总览'):
                    switch_step = 0

            if not emulator.find_img(f'干员空位'):
                if emulator.find_img(f'控制中枢'):
                    break
                if emulator.find_img(f'在进驻总览'):
                    emulator.swipe((1216, 158, 1215, 450))
                    time.sleep(1)
    pass