# TP Recovery Automation

## How It Works

The TP recovery automation is **conditional** - it only activates when the game prompts you to recover TP.

### When Does TP Recovery Happen?

- ✅ **Only when TP is empty** and the game shows the recovery prompt
- ✅ The automation detects the "回復する" (recover) button
- ✅ If TP is not empty, these screens never appear and are skipped

### What Item Does It Use?

⚠️ **IMPORTANT:** The automation **ALWAYS** uses the **BOTTLE (タフネス30)**

This is specifically the **SECOND option** in the TP recovery items list.

### The Flow

When TP recovery is needed:

1. **Detect TP Recovery Prompt** - Looks for "回復する" button
2. **Click Recovery** - Clicks "回復する" (recover)
3. **Select Bottle** - Finds and clicks the BOTTLE item (タフネス30)
4. **Click Use Button** - Clicks "使う" (use) for the bottle
5. **Confirm Quantity** - Clicks OK to confirm

### Template Files

The automation uses these templates for TP recovery:

- `kaifuku_button.png` - The "回復する" (recover) button
- `bottle_item.png` - The bottle item (タフネス30) - SECOND in list
- `bottle_use_button.png` - The "使う" (use) button for bottle
- `ok_button.png` - OK confirmation button

### In Sequence Mode

```python
# These are all marked as OPTIONAL
(GameScreen.TP_RECOVERY_CONFIRM, ...)   # Only if TP empty
(GameScreen.TP_RECOVERY_ITEMS, ...)     # Selects BOTTLE
(GameScreen.ITEM_QUANTITY, ...)         # Confirms quantity
```

If TP is full, the automation will:
- ✅ Skip these screens entirely
- ✅ Continue to the next step (event skip settings)
- ✅ No errors or warnings

### In Continuous Mode

The automation continuously monitors for TP recovery prompts:

```python
elif current_screen == GameScreen.TP_RECOVERY_CONFIRM:
    self.handle_tp_recovery_confirm()  # Clicks "回復する"
elif current_screen == GameScreen.TP_RECOVERY_ITEMS:
    self.handle_tp_recovery_items()     # Selects BOTTLE
elif current_screen == GameScreen.ITEM_QUANTITY:
    self.handle_item_quantity()         # Confirms OK
```

Whenever the TP recovery prompt appears (during training), it will automatically:
1. Detect the prompt
2. Use a bottle to recover TP
3. Continue training

## Why the Bottle?

The bottle (タフネス30) is:
- ✅ Common and easy to obtain
- ✅ Always the second option in the list
- ✅ Recovers exactly 30 TP
- ✅ Most reliable for automation

## What If You Run Out of Bottles?

If you run out of bottles:
- ❌ The automation will fail to find the bottle template
- ❌ It will try the fallback "use" button
- ⚠️ **You should manually handle this or stop the automation**

**Recommendation:** Make sure you have enough bottles before running long automation sessions!

## Customizing the Item

If you want to use a different item:

1. Take a screenshot of your preferred item
2. Crop just the item (like the bottle template)
3. Replace `templates/bottle_item.png` with your item
4. Replace `templates/bottle_use_button.png` with the "使う" button for that item

The automation will then use your preferred item instead.

## Debug Mode

Enable debug mode to see what's happening during TP recovery:

```yaml
# config.yaml
debug: true
```

This will save screenshots at each step:
- `debug_tp_confirm_*.png` - When recovery prompt appears
- `debug_tp_items_*.png` - When selecting the bottle
- `debug_item_quantity_*.png` - When confirming quantity

Check these if the automation isn't working correctly.
