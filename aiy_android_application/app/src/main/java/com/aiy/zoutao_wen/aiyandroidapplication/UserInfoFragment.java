package com.aiy.zoutao_wen.aiyandroidapplication;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class UserInfoFragment extends Fragment {
    private User user;
    private TextView id_tv;
    private TextView fname_tv;
    private TextView lname_tv;
    private TextView email_tv;
    private TextView role_tv;
    private TextView creat_time_tv;
    private TextView expir_time_tv;
    private TextView usr_desp_tv;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.user_info_fragment, container, false);
    }

    @Override
    public void onStart(){//after onCreateView
        super.onStart();
        id_tv = (TextView) getView().findViewById(R.id.id_tv);
        fname_tv = (TextView) getView().findViewById(R.id.fname_tv);
        lname_tv = (TextView) getView().findViewById(R.id.lname_tv);
        email_tv = (TextView) getView().findViewById(R.id.email_tv);
        role_tv = (TextView) getView().findViewById(R.id.role_tv);
        creat_time_tv = (TextView) getView().findViewById(R.id.creat_time_tv);
        expir_time_tv = (TextView) getView().findViewById(R.id.expir_time_tv);
        usr_desp_tv = (TextView) getView().findViewById(R.id.usr_desp_tv);
        refreshView(user);
    }

    @Override
    public void onAttach(Activity activity){ //ahead of onCreateView
        super.onAttach(activity);
        user = ((MenuActivity)activity).getUser();
    }

    private void refreshView(User user){
        id_tv.setText(user.getId());
        fname_tv.setText(user.getFname());
        lname_tv.setText(user.getLname());
        email_tv.setText(user.getE_mail());
        role_tv.setText(user.getRole());
        creat_time_tv.setText(user.getCreation_time());
        expir_time_tv.setText(user.getExpiration_time());
        usr_desp_tv.setText(user.getUser_description());
    }
}
