package kerbianbridge.android;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;
import android.app.AlertDialog;
import android.graphics.BitmapFactory;
import android.graphics.Bitmap;
import android.os.Handler;
import android.os.Looper;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.HashMap;

public class UIManager {
    private final HashMap<Integer, View> views = new HashMap<>();
    private int nextId = 1;
    private final Context context;
    private final ViewGroup rootLayout;

    public UIManager(Context ctx, ViewGroup root) {
        context = ctx;
        rootLayout = root;
    }

    public int createView(String type, JSONObject props) {
        try {
            View v = null;
            int id = nextId++;
            switch (type) {
                case "Button":
                    Button btn = new Button(context);
                    btn.setText(props.optString("text", ""));
                    btn.setId(id);
                    btn.setOnClickListener(view -> BridgeEventRouter.emit("onPress", id, null));
                    v = btn;
                    break;
                case "Text":
                    TextView tv = new TextView(context);
                    tv.setText(props.optString("value", ""));
                    tv.setId(id);
                    v = tv;
                    break;
                case "Image":
                    ImageView iv = new ImageView(context);
                    String path = props.optString("src", "");
                    if (!path.isEmpty()) {
                        Bitmap bmp = BitmapFactory.decodeFile(path);
                        iv.setImageBitmap(bmp);
                    }
                    iv.setId(id);
                    v = iv;
                    break;
                case "List":
                    ListView lv = new ListView(context);
                    JSONArray items = props.optJSONArray("items");
                    if (items != null) {
                        String[] data = new String[items.length()];
                        for (int i = 0; i < items.length(); i++) {
                            data[i] = items.getString(i);
                        }
                        ArrayAdapter<String> adapter = new ArrayAdapter<>(context, android.R.layout.simple_list_item_1, data);
                        lv.setAdapter(adapter);
                        lv.setOnItemClickListener((adapterView, view, i, l) ->
                            BridgeEventRouter.emit("onItemPress", id, new JSONObject().put("index", i))
                        );
                    }
                    lv.setId(id);
                    v = lv;
                    break;
                case "Modal":
                    String message = props.optString("message", "");
                    Handler handler = new Handler(Looper.getMainLooper());
                    handler.post(() -> {
                        AlertDialog.Builder builder = new AlertDialog.Builder(context);
                        builder.setMessage(message);
                        builder.setPositiveButton("OK", (dialog, which) ->
                            BridgeEventRouter.emit("onModalClose", -1, null)
                        );
                        builder.setCancelable(false);
                        AlertDialog dlg = builder.create();
                        dlg.show();
                    });
                    return -1;
                default:
                    ErrorReporter.report("UIError", "Unknown view type: " + type, new JSONObject());
                    return -1;
            }
            views.put(id, v);
            Handler handler = new Handler(Looper.getMainLooper());
            handler.post(() -> rootLayout.addView(v));
            return id;
        } catch (Exception e) {
            ErrorReporter.report("UIError", "Failed to create view: " + type, new JSONObject().put("exception", e.toString()));
            return -1;
        }
    }

    public void updateView(int id, JSONObject props) {
        try {
            View v = views.get(id);
            if (v == null) {
                ErrorReporter.report("UIError", "View not found for update: " + id, new JSONObject());
                return;
            }
            if (v instanceof TextView && props.has("value")) {
                ((TextView) v).setText(props.optString("value", ""));
            } else if (v instanceof Button && props.has("text")) {
                ((Button) v).setText(props.optString("text", ""));
            } else if (v instanceof ImageView && props.has("src")) {
                Bitmap bmp = BitmapFactory.decodeFile(props.optString("src", ""));
                ((ImageView) v).setImageBitmap(bmp);
            }
        } catch (Exception e) {
            ErrorReporter.report("UIError", "Failed to update view: " + id, new JSONObject().put("exception", e.toString()));
        }
    }

    public void removeView(int id) {
        try {
            View v = views.get(id);
            if (v != null) {
                Handler handler = new Handler(Looper.getMainLooper());
                handler.post(() -> rootLayout.removeView(v));
                views.remove(id);
            } else {
                ErrorReporter.report("UIError", "View not found for removal: " + id, new JSONObject());
            }
        } catch (Exception e) {
            ErrorReporter.report("UIError", "Failed to remove view: " + id, new JSONObject().put("exception", e.toString()));
        }
    }

    public View getView(int id) {
        return views.get(id);
    }
}