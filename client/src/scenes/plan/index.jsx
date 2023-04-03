import { useState } from "react";
import { formatDate } from "@fullcalendar/core";
import FullCalendar from "@fullcalendar/react";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import interactionPlugin from "@fullcalendar/interaction";
import listPlugin from "@fullcalendar/list";
import {
  Box,
  List,
  ListItem,
  ListItemText,
  Typography,
  useTheme,
} from "@mui/material";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const ResourceCalendar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [currentEvents, setCurrentEvents] = useState([]);

  const resources = [
    { id: "1", title: "Nick Gerr" },
    { id: "2", title: "Peter Enis" },
    { id: "3", title: "Vetter Dick Karsch" },
    { id: "3", title: "Axel Schweiß" },
  ];

  const handleDateClick = (selected) => {
    const title = prompt("Please enter a new title for your event");
    const calendarApi = selected.view.calendar;
    calendarApi.unselect();

    if (title) {
      calendarApi.addEvent({
        id: `${selected.dateStr}-${title}`,
        title,
        start: selected.startStr,
        end: selected.endStr,
        allDay: selected.allDay,
        resourceId: resources[0].id, // Assign to first resource by default
      });
    }
  };

  const handleEventClick = (selected) => {
    if (
      window.confirm(
        `Are you sure you want to delete the event '${selected.event.title}'`
      )
    ) {
      selected.event.remove();
    }
  };

  return (
    <Box m="20px">
      <Header title="Resource Calendar" subtitle="Resource Planning Calendar" />

      <Box display="flex" justifyContent="space-between">
        {/* CALENDAR SIDEBAR */}
        <Box
          flex="1 1 20%"
          backgroundColor={colors.primary[400]}
          p="15px"
          borderRadius="4px"
        >
          <Typography variant="h5">Resources</Typography>
          <List>
            {resources.map((resource) => (
              <ListItem
                key={resource.id}
                sx={{
                  backgroundColor: colors.greenAccent[500],
                  margin: "10px 0",
                  borderRadius: "2px",
                }}
              >
                <ListItemText primary={resource.title} />
              </ListItem>
            ))}
          </List>
        </Box>

        {/* CALENDAR */}
        <Box flex="1 1 100%" ml="15px">
          <FullCalendar
            height="75vh"
            plugins={[resourceTimelinePlugin, interactionPlugin, listPlugin]}
            headerToolbar={{
              left: "prev,next today",
              center: "title",
              right:
                "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth,listMonth",
            }}
            initialView="resourceTimelineWeek"
            editable={true}
            selectable={true}
            selectMirror={true}
            dayMaxEvents={true}
            resources={resources}
            select={handleDateClick}
            eventClick={handleEventClick}
            eventsSet={(events) => setCurrentEvents(events)}
            initialEvents={[
              {
                id: "12315",
                title: "Event 1",
                start: "2022-09-14T09:00:00",
                end: "2022-09-14T12:00:00",
                resourceId: "1",
              },
              {
                id: "5123",
                title: "Event 2",
                start: "2022-09-28T14:00:00",
                end: "2022-09-28T16:00:00",
                resourceId: "2",
              },
              {
                id: "5412",
                title: "Event 3",
                start: "2022-09-30T10:00:00",
                end: "2022-09-30T14:00:00",
                resourceId: "3",
              },
              {
                id: "5417",
                title: "Event 4",
                start: "2022-09-30T10:00:00",
                end: "2022-09-30T14:00:00",
                resourceId: "4",
              },
            ]}
          />
        </Box>
      </Box>
    </Box>
  );
};

export default ResourceCalendar;
