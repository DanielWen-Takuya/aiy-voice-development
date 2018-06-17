package com.aiy.zoutao_wen.aiyandroidapplication;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MainActivity extends AppCompatActivity implements DownloadCallback<String>{


    // Boolean telling us whether a download is in progress, so we don't trigger overlapping
    // downloads with consecutive button clicks.
    private boolean mDownloading = false;

    private DownloadTask mDownloadTask;

    private EditText email;
    private EditText password;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        email = (EditText) findViewById(R.id.email_input);
        password = (EditText) findViewById(R.id.password_input);
        mDownloadTask = new DownloadTask(this);
        mDownloadTask.execute("http://192.168.1.26:5000/");
    }

    public void enterClicked(View v){
        Toast.makeText(this, "Checking the log in information!", Toast.LENGTH_SHORT).show();
        String execution = "http://192.168.1.26:5000/login?email=" + email.getText() +
                "&password=" + md5(password.getText().toString());
        mDownloadTask = new DownloadTask(this);
        mDownloadTask.execute(execution);
    }

    @Override
    public void updateFromDownload(String result) {
        //final String result_e = result;
        String action;
        Boolean status;
        Toast.makeText(this, result, Toast.LENGTH_SHORT).show();
        try {
            JSONObject json_result = new JSONObject(result);
            action = json_result.getString("action");
            status = json_result.getBoolean("status");
            if(action.equals("check")){
                if(status)
                    Toast.makeText(this,"Server is active",Toast.LENGTH_SHORT).show();
                else{//will never be here
                    AlertDialog alertDialog = new AlertDialog.Builder(MainActivity.this).create();
                    alertDialog.setTitle("Alert");
                    alertDialog.setMessage("Please check the server");
                    alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                            new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    dialog.dismiss();
                                }
                            });
                    alertDialog.show();
                }
            }else if(action.equals("login")){
                if(status){
                    //enter here
                    String user = json_result.getString("email");
                    Toast.makeText(this,"Welcome " + user + " !",Toast.LENGTH_SHORT).show();
                }else{
                    Toast.makeText(this,"Wrong email or password",Toast.LENGTH_SHORT).show();
                }
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }


        /*runOnUiThread(new Runnable() {
            @Override
            public void run() {
                e.setText(result_e);
            }
        });*/
    }

    @Override
    public NetworkInfo getActiveNetworkInfo() {
        ConnectivityManager connectivityManager =
                (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();
        return networkInfo;
    }

    @Override
    public void onProgressUpdate(int progressCode, int percentComplete) {
        switch(progressCode) {
            // You can add UI behavior for progress updates here.
            case Progress.ERROR:
                break;
            case Progress.CONNECT_SUCCESS:
                break;
            case Progress.GET_INPUT_STREAM_SUCCESS:
                break;
            case Progress.PROCESS_INPUT_STREAM_IN_PROGRESS:
                break;
            case Progress.PROCESS_INPUT_STREAM_SUCCESS:
                break;
        }
    }

    @Override
    public void finishDownloading() {
        mDownloading = false;
    }

    public static String md5(String content) {
        byte[] hash;
        try {
            hash = MessageDigest.getInstance("MD5").digest(content.getBytes("UTF-8"));
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("NoSuchAlgorithmException",e);
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("UnsupportedEncodingException", e);
        }

        StringBuilder hex = new StringBuilder(hash.length * 2);
        for (byte b : hash) {
            if ((b & 0xFF) < 0x10){
                hex.append("0");
            }
            hex.append(Integer.toHexString(b & 0xFF));
        }
        return hex.toString();
    }
}


