package com.aiy.zoutao_wen.aiyandroidapplication;

import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MenuActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener ,DownloadCallback<String>{

    private DownloadTask mDownloadTask;
    private boolean mDownloading = false;

    private TextView user_name_tv;
    private TextView user_email_tv;

    private String user_id;//user_id id
    private User user;

    private FragmentManager mFragmentManager;
    private FragmentTransaction mFragmentTransaction;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        mFragmentManager= getFragmentManager();
        FragmentTransaction fragmentTransaction = mFragmentManager.beginTransaction();
        WelcomeFragment welcomeFragment = new WelcomeFragment();
        fragmentTransaction.add(R.id.fragment_container,welcomeFragment);
        fragmentTransaction.commit();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        View headerView = navigationView.getHeaderView(0);
        user_name_tv = (TextView)headerView.findViewById(R.id.user_name);
        user_email_tv = (TextView)headerView.findViewById(R.id.user_email);

        user_id = getIntent().getStringExtra("USER_ID");
        String execution = "http://192.168.1.26:5000/getUserInfo?id=" + user_id;
        mDownloadTask = new DownloadTask(this);
        mDownloadTask.execute(execution,"GET");


    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_data_obs) {
            FragmentTransaction fragmentTransaction = mFragmentManager.beginTransaction();
            DataObservationFragment dataObservationFragment = new DataObservationFragment();
            fragmentTransaction.replace(R.id.fragment_container,dataObservationFragment);
            fragmentTransaction.addToBackStack(null);
            fragmentTransaction.commit();
        } else if (id == R.id.nav_data_graph) {
            FragmentTransaction fragmentTransaction = mFragmentManager.beginTransaction();
            DataGraphFragment dataGraphFragment = new DataGraphFragment();
            fragmentTransaction.replace(R.id.fragment_container,dataGraphFragment);
            fragmentTransaction.addToBackStack(null);
            fragmentTransaction.commit();
        } else if (id == R.id.nav_play_music) {
            FragmentTransaction fragmentTransaction = mFragmentManager.beginTransaction();
            PlayMusicFragment playMusicFragment = new PlayMusicFragment();
            fragmentTransaction.replace(R.id.fragment_container,playMusicFragment);
            fragmentTransaction.addToBackStack(null);
            fragmentTransaction.commit();
        } else if (id == R.id.nav_user_info) {
            FragmentTransaction fragmentTransaction = mFragmentManager.beginTransaction();
            UserInfoFragment userInfoFragment = new UserInfoFragment();
            fragmentTransaction.replace(R.id.fragment_container,userInfoFragment);
            fragmentTransaction.addToBackStack(null);
            fragmentTransaction.commit();
        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    @Override
    public void finishDownloading() {
        mDownloading = false;
    }

    @Override
    public void updateFromDownload(String result) {
        //final String result_e = result;
        String action;
        Boolean status;
        //Toast.makeText(this, result, Toast.LENGTH_SHORT).show();
        try {
            JSONObject json_result = new JSONObject(result);
            action = json_result.getString("action");
            status = json_result.getBoolean("status");
            if(action.equals("logout")){
                if(status){
                    Toast.makeText(this,"Id " + user_id + " logout success!",Toast.LENGTH_SHORT).show();
                }else{
                    Toast.makeText(this,"Logout failed! Contact to administrator",Toast.LENGTH_SHORT).show();
                }
            }else if(action.equals("getUserInfo")){
                if(status){
                    Toast.makeText(this,"Get Id " + user_id + " info success!",Toast.LENGTH_SHORT).show();
                    JSONArray user_info = json_result.getJSONArray("userInfo");
                    user = new User(user_id, user_info.get(0).toString(),user_info.get(1).toString(),
                            user_info.get(2).toString(),user_info.get(3).toString(),
                            user_info.get(4).toString(),user_info.get(5).toString(),
                            user_info.get(6).toString());
                    //Toast.makeText(this,"Test:" + user.getFname(),Toast.LENGTH_SHORT).show();

                    //not update textView info here
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            String full_name = user.getFname() + " " + user.getLname();
                            String email = user.getE_mail();
                            user_name_tv.setText(full_name);
                            user_email_tv.setText(email);
                        }
                    });

                }else{
                    Toast.makeText(this,"Failed to get Id " + user_id + " info !",Toast.LENGTH_SHORT).show();
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
    public void onStop(){
        super.onStop();
        String execution = "http://192.168.1.26:5000/logout?id=" + user_id;
        mDownloadTask = new DownloadTask(this);
        mDownloadTask.execute(execution,"DELETE");
    }
}
