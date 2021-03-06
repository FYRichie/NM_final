import React from "react";
import { ListItemIcon, ListItemButton, ListItemText, List } from "@mui/material";
import AccessAlarmIcon from "@mui/icons-material/AccessAlarm";
import SettingsIcon from "@mui/icons-material/Settings";

const list = [
    { text: "Timer", icon: <AccessAlarmIcon /> },
    { text: "Setting", icon: <SettingsIcon /> },
];

export default (props) => {
    const changeDisplay = props["changeDisplay"];

    const listItem = (item) => (
        <ListItemButton
            onClick={() => {
                console.log(`Select display ${item["text"]}`);
                changeDisplay(item["text"]);
            }}>
            <ListItemIcon>{item["icon"]}</ListItemIcon>
            <ListItemText primary={item["text"]} />
        </ListItemButton>
    );

    return <React.Fragment>{list.map((item) => listItem(item))}</React.Fragment>;
};
